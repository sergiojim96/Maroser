from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from ..models import OrderItem
from ..models import Order
from ..models import Item
from ..models import UserProfile
from ..forms import CouponForm
from django.core.exceptions import ObjectDoesNotExist
from ..views.PayPalClient import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest
from paypalcheckoutsdk.payments import AuthorizationsGetRequest, AuthorizationsVoidRequest, AuthorizationsCaptureRequest

import operator


class Get_Order(PayPalClient):

    def pay(self, orderID, authorizationID, order):
        orderTotal, tax, shipping = order.get_total()
        payPalOrder = OrdersGetRequest(orderID)
        payPalAutorization = AuthorizationsGetRequest(authorizationID)
        responseOrderDetails = self.client.execute(payPalOrder)
        responseAuthorizationsDetails = self.client.execute(payPalAutorization)

        if ((responseOrderDetails.result.purchase_units[0].amount.value == str(orderTotal)) &
                (responseOrderDetails.result.purchase_units[0].amount.currency_code == "USD")):
            payPalCaptureRequest = AuthorizationsCaptureRequest(authorizationID)
            responsePayPalCapture = self.client.execute(payPalCaptureRequest)
            status = responsePayPalCapture.status_code
            if (status == 200)|(status == 201):
                dabaBundle = {'status': 'Nice'}
                order.ordered = True
                try:
                    user_profile = UserProfile.objects.create(
                        email=responseOrderDetails.result.purchase_units[0].payee.email_address,
                        provincia=responseOrderDetails.result.purchase_units[0].shipping.address.admin_area_1,
                        canton=responseOrderDetails.result.purchase_units[0].shipping.address.admin_area_2,
                        address=responseOrderDetails.result.purchase_units[0].shipping.address.address_line_1,
                        distrito=responseOrderDetails.result.purchase_units[0].shipping.address.address_line_2)
                except AttributeError:
                    user_profile = UserProfile.objects.create(
                        email=responseOrderDetails.result.purchase_units[0].payee.email_address,
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
            total, tax, shipping = order.get_total()
            maybeObjects = filter(lambda x: x.label == 'M', Item.objects.all())
            context = {
                'object': order,
                'total': total,
                'tax': tax,
                'maybeObjects': maybeObjects,
                'shipping': shipping,
                'email': order.user_profile.email,
                'provincia': order.user_profile.provincia,
                'canton': order.user_profile.canton,
                'distrito': order.user_profile.distrito,
                'address': order.user_profile.address,
            }
            return render(request, 'resume.html', context)


    def pay(request, orderID, authorizationID):
        x = Get_Order()
        order_qs = Order.objects.filter(
            user=request.session.session_key,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            return x.pay(orderID, authorizationID, order)

    def get(self, *args, **kwargs):
        try:
            total = 0
            order = Order.objects.get(user=self.request.session.session_key, ordered=False)
            total, tax, shipping = order.get_total()
            maybeObjects = filter(self.is_maybe_object, Item.objects.all())
            context = {
                'object': order,
                'total': total,
                'tax': tax,
                'maybeObjects': maybeObjects,
                'shipping': shipping
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

    def is_maybe_object(self, item):
        if item.label == 'M':
            return True
        else:
            return False

    def add_single_item_to_cart(request, slug):
        if request.is_ajax() and request.method == "GET":
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
                    order_item.quantity += 1
                    order_item.save()
                    total, tax, shipping = order.get_total()
                    itemPrice = order_item.get_total_item_price()
                    dataBundle = {"total": total, "tax": tax, "itemPrice": itemPrice, "slug": slug,
                                  "shipping": shipping}
                    return JsonResponse({"scc": "true", "dataBundle": dataBundle}, status=200)
                else:
                    return JsonResponse({"scc": "false"}, status=200)
            else:
                return JsonResponse({"scc": "false"}, status=200)
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
                    return JsonResponse({"scc": "true"}, status=200)
                else:
                    return JsonResponse({"scc": "false"}, status=200)
            else:
                return JsonResponse({"scc": "false"}, status=200)
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
                    return JsonResponse({"scc": "true", "dataBundle": dataBundle}, status=200)
                else:
                    return JsonResponse({"scc": "false"}, status=400)
            else:
                return JsonResponse({"scc": "false"}, status=400)
        else:
            return JsonResponse({}, status=400)
