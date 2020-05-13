from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from ..forms import CouponForm
from ..models import Coupon
from ..models import Order

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.session.session_key, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")
                
    def get_coupon(request, code):
        try:
            coupon = Coupon.objects.get(code=code)
            return coupon
        except ObjectDoesNotExist:
            messages.info(request, "This coupon does not exist")
            return redirect("core:checkout")