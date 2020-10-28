from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from ..models import OrderItem
from ..models import Order
from ..models import Item
from ..forms import CouponForm
from django.core.exceptions import ObjectDoesNotExist
import operator

class OrderSummaryView(View):
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
                    total, tax, shipping = order.get_total()
                    itemPrice = order_item.get_total_item_price()
                    dataBundle = {"total" : total, "tax" : tax, "itemPrice" : itemPrice, "slug" : slug, "shipping" : shipping}
                    return JsonResponse({"scc": "true", "dataBundle" : dataBundle}, status=200)
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
                    dataBundle = {"total" : total, "tax" : tax, "itemPrice" : itemPrice, "slug" : slug,"shipping" : shipping}
                    return JsonResponse({"scc": "true", "dataBundle" : dataBundle}, status=200)
                else:
                    return JsonResponse({"scc": "false"}, status=400)
            else:
                return JsonResponse({"scc": "false"}, status=400)
        else:
            return JsonResponse({}, status=400)
