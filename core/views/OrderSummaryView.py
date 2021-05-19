from reportlab.lib.colors import lightgrey, red, blue, lightblue
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from reportlab.platypus import Table, TableStyle
from django.http.response import JsonResponse
from reportlab.lib.colors import HexColor
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from datetime import datetime, date
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from django.conf import settings
from ..models import UserProfile
from reportlab.lib import colors
from reportlab.lib import colors
from ..forms import CouponForm
from ..models import OrderItem
from ..models import Order
from ..models import Item
from django.core.exceptions import ObjectDoesNotExist
from ..views.PayPalClient import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest
from paypalcheckoutsdk.payments import AuthorizationsGetRequest, AuthorizationsVoidRequest, AuthorizationsCaptureRequest
import operator


class Get_Order(PayPalClient):

    def pay(self, orderID, authorizationID, order):
        orderTotal  = order.get_total()
        payPalOrder = OrdersGetRequest(orderID)

        responseOrderDetails = self.client.execute(payPalOrder)
        if ((float(responseOrderDetails.result.purchase_units[0].amount.value) == orderTotal) &
                (responseOrderDetails.result.purchase_units[0].amount.currency_code == "USD")):
            payPalCaptureRequest = AuthorizationsCaptureRequest(authorizationID)
            responsePayPalCapture = self.client.execute(payPalCaptureRequest)
            status = responsePayPalCapture.status_code
            if (status == 200)|(status == 201):
                dabaBundle = {'status': 'Nice'}
                order.ordered = True
                try:
                    user_profile = UserProfile.objects.create(
                        user=order.user,
                        email=responseOrderDetails.result.payer.email_address,
                        provincia=responseOrderDetails.result.purchase_units[0].shipping.address.admin_area_1,
                        canton=responseOrderDetails.result.purchase_units[0].shipping.address.admin_area_2,
                        address=responseOrderDetails.result.purchase_units[0].shipping.address.address_line_1,
                        distrito=responseOrderDetails.result.purchase_units[0].shipping.address.address_line_2)
                except AttributeError:
                    user_profile = UserProfile.objects.create(
                        user=order.user,
                        email=responseOrderDetails.result.payer.email_address,
                        provincia=responseOrderDetails.result.purchase_units[0].shipping.address.admin_area_1,
                        canton=responseOrderDetails.result.purchase_units[0].shipping.address.admin_area_2,
                        address=responseOrderDetails.result.purchase_units[0].shipping.address.address_line_1)

                order.user_profile = user_profile
                order.save()

                return JsonResponse({"scc": "true", "dataBundle": dabaBundle}, status=200)
            else:
                dabaBundle = {'status': 'PaypalCaptureError'}
                return JsonResponse({"scc": "false", "dataBundle": dabaBundle}, status=400)
        else:
            voidRequest = AuthorizationsVoidRequest(authorizationID)
            responsePayPalVoid = self.client.execute(voidRequest)
            dabaBundle = {'status': 'AttemptedFraud'}
            return JsonResponse({"scc": "false", "dataBundle": dabaBundle}, status=400)




class OrderSummaryView(View):

    def resume(request):
        order_qs = Order.objects.filter(
            user=request.session.session_key,
            ordered=True
        )
        if order_qs.exists():
            order = order_qs[0]
            total = order.get_total()
            maybeObjects = filter(lambda x: x.label == 'M', Item.objects.all())
            context = {
                'object': order,
                'total': total,
                'maybeObjects': maybeObjects,
                'email': order.user_profile.email,
                'provincia': order.user_profile.provincia,
                'canton': order.user_profile.canton,
                'distrito': order.user_profile.distrito,
                'address': order.user_profile.address,
            }
            OrderSummaryView.sendmail(context)
            return render(request, 'resume.html', context)
        return render(request, 'resume.html', {})


    def pay(request, orderID, authorizationID):
        paypalOrder = Get_Order()
        order_qs = Order.objects.filter(
            user=request.session.session_key,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            return paypalOrder.pay(orderID, authorizationID, order)
        else:
            return JsonResponse({"scc": "false"}, status=400)

    def hasActiveOrder(request):
        order_qs = Order.objects.filter(
            user=request.session.session_key,
            ordered=False
        )
        if order_qs.exists():
            return JsonResponse({"scc": "true"}, status=200)
        else:
            return JsonResponse({"scc": "false"}, status=400)

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.session.session_key, ordered=False)
            total = order.get_total()
            maybeObjects = filter(self.is_maybe_object, Item.objects.all())
            context = {
                'object': order,
                'total': total,
                'maybeObjects': maybeObjects
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/catalog/")

    def is_maybe_object(self, item):
        if item.label == 'M':
            return True
        else:
            return False

    def add_single_item_to_cart(request, slug):
        # Import the Secret Manager client library.

        item = get_object_or_404(Item, slug=slug)
        if request.is_ajax() and request.method == "GET":
            order_qs = Order.objects.filter(
                user=request.session.session_key,
                ordered=False
            )
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.items.filter(item__slug=item.slug).exists():
                    order_item = OrderItem.objects.filter(
                        item=item,
                        user=request.session.session_key,
                        ordered=False
                    )[0]
                    order_item.quantity += 1
                    order_item.save()
                    total = order.get_total()
                    itemPrice = order_item.get_total_item_price()
                    dataBundle = {"total": total, "tax": 0, "itemPrice": itemPrice, "slug": slug,
                                  "shipping": 0}
                    return JsonResponse({"scc": "Ok", "dataBundle": dataBundle}, status=200)
                else:
                    return JsonResponse({"scc": "NotInOrder"}, status=200)
            else:
                return JsonResponse({"scc": "OrderNotExists"}, status=200)
        else:
            return JsonResponse({}, status=400)

    def async_remove_from_cart(request):
        if request.is_ajax() and request.method == "GET":
            slug = request.GET.get("slug")
            item = get_object_or_404(Item, slug=slug)
            order_qs = Order.objects.filter(
                user=request.session.session_key,
                ordered=False
            )
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.items.filter(item__slug=item.slug).exists():
                    order_item = OrderItem.objects.filter(
                        item=item,
                        user=request.session.session_key,
                        ordered=False
                    )[0]
                    order.items.remove(order_item)
                    order_item.delete()
                    return JsonResponse({"scc": "Ok"}, status=200)
                else:
                    return JsonResponse({"scc": "NotInOrder"}, status=200)
            else:
                print("notexists")
                return JsonResponse({"scc": "OrderNotExists"}, status=200)
        else:
            return JsonResponse({}, status=400)

    def remove_single_item_from_cart(request, slug):
        if request.is_ajax() and request.method == "GET":
            item = get_object_or_404(Item, slug=slug)
            order_qs = Order.objects.filter(
                user=request.session.session_key,
                ordered=False
            )
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.items.filter(item__slug=slug).exists():
                    order_item = OrderItem.objects.filter(
                        item=item,
                        user=request.session.session_key,
                        ordered=False
                    )[0]
                    if order_item.quantity > 1:
                        order_item.quantity -= 1
                        order_item.save()
                    else:
                        order.items.remove(order_item)
                    total, tax, shipping = order.get_total()
                    itemPrice = order_item.get_total_item_price()
                    dataBundle = {"total": total, "tax": tax, "itemPrice": itemPrice, "slug": slug,
                                  "shipping": shipping}
                    return JsonResponse({"scc": "Ok", "dataBundle": dataBundle}, status=200)
                else:
                    return JsonResponse({"scc": "NotInOrder"}, status=200)
            else:
                return JsonResponse({"scc": "OrderNotExists"}, status=200)
        else:
            return JsonResponse({}, status=400)

    def sendmail(context):
        pdfDirName = OrderSummaryView.creatInvoice(context)
        email = EmailMessage(
        'SashaCollections gracias por tu compra', OrderSummaryView.getMailMessage(), settings.EMAIL_HOST_USER, [context['email']])
        email.attach_file(pdfDirName)
        email.send()
    
    def getMailMessage():
        message = f'''Gracias por confiar en nosotros para tu compra.
Adjunto a este correo encontraras un documento PDF con la factura de tu compra

Atte,

Sasha colelctions'''
        return message

    def getXDifference(i):
        switcher = {
            1: 20,
            2: -4
        }
        return switcher.get(i, 0)

    def creatInvoice(context):
        data = OrderSummaryView.getData(context["object"])
        size = len(data)
        pdfDirName = f"Facturas\{context['object'].ref_code}.pdf"
        c = canvas.Canvas(pdfDirName,pagesize=(200,250),bottomup=0)
        c.setFont("ZapfDingbats",8)
        c.setFillColor(colors.salmon)
        # bloque sasha collection y lineas de recibo
        c.translate(-60,0)
        c.drawString(65,20,"S")
        c.setFont("Courier-Bold",8)
        c.setFillColor(HexColor('#1e5262'))
        c.drawCentredString(115,20,"SASHA'S COLLECTION")
        c.translate(40,28)
        c.setFillColor(colors.salmon)
        c.setStrokeColor(colors.salmon)
        c.rect(0.2*cm,0.2*cm,4.7*cm,0.1*cm, fill=1)
        c.setFillColor(HexColor('#1e5262'))
        c.drawCentredString(160,10,"RECIBO")
        c.setFillColor(colors.salmon)
        c.setStrokeColor(colors.salmon)
        c.translate(170,0)
        c.rect(0.4*cm,0.2*cm,2*cm,0.1*cm, fill=1)

        c.translate(-155, -45)
        c.setFont("Helvetica-Bold",5)
        c.setFillColor(HexColor('#1e5262'))
        # bloque de informacion
        c.drawString(13,70,"Información general")
        c.translate(-15,10)
        c.setFont("Times-Italic",5)
        c.drawString(28,70,"Cod. DE RECIBO: " + context["object"].ref_code)
        c.drawString(28,80,"CORREO :" + context["email"])
        c.drawString(28,90,"FECHA :" + context["object"].ordered_date.strftime('%d-%m-%y'))
        c.setStrokeColor(colors.salmon)
        c.translate(5,95)
        # Initial value of Y = 0.2
        list = OrderSummaryView.getYValuesList(0.2, size)
        c.setFont("Helvetica-Bold",5)
        c.setLineWidth(0.5)
        # Bloque de items
        c.grid([0.8*cm, 1.7*cm, 3.8*cm, 5.6*cm, 6.6*cm], list)
        c.drawCentredString(34,12,"CANT.")
        c.drawCentredString(75,12,"PRODUCTO")
        c.drawCentredString(133,12,"PRECIO UNITARIO")
        c.drawCentredString(173,12,"TOTAL")
        c.setFont("Times-Italic",5)
        c.translate(34, 21)
        acx = 0
        for i in range(0, size):
            for index, val in enumerate(data[i]):
                dif = OrderSummaryView.getXDifference(index)
                c.drawCentredString(acx, 0, str(val))
                acx += 41 + dif
            c.translate(0, 8)
            acx = 0
            dif = 0
        c.translate(107,10)
        c.setFont("Helvetica-Bold",5)
        c.drawCentredString(0, 0, "TOTAL")
        c.drawCentredString(38, 0, f"$ {str(context['total'])}")

        # necesario para paginacion
        c.showPage()
        # guardar en disco
        c.save()
        return pdfDirName
    
    def getData(order):
        finalList = []
        itemList = []
        for orderItem in order.items.all():
            itemList.append(str(orderItem.quantity))
            itemList.append(orderItem.item.title)
            itemList.append(str(orderItem.item.price))
            itemList.append(str(orderItem.quantity*orderItem.item.price))
            finalList.append(itemList)
            itemList = []
        return finalList

    def getYValuesList(y, size):
        values = []
        for i in range(0,size+2):
            values.append(y*cm)
            y += 0.3
        return values
