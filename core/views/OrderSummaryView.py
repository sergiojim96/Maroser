from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from ..models import Order
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