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

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            total = 0
            order = Order.objects.get(user=self.request.session.session_key, ordered=False)
            total, tax = order.get_total()
            context = {
                'object': order,
                'total': total,
                'tax' : tax
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

    def async_remove_from_cart(request):
        if request.is_ajax() and request.method == "GET":
            slug = request.GET.get("slug")
            item = get_object_or_404(Item, slug=slug)
            print(item.slug)
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