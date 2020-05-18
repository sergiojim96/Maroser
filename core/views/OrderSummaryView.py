from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from ..models import Order
from django.core.exceptions import ObjectDoesNotExist

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.session.session_key, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")