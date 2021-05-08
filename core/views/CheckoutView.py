from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.http.response import JsonResponse
from .PayPalClient import PayPalClient
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from ..forms import CheckoutForm
from ..models import OrderItem
from ..forms import CouponForm
from ..models import Address
from ..models import Order
from ..models import Item
import string 
import random


def create_ref_code():
    while True:
        ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        order = Order.objects.filter(ref_code=ref_code)
        if not order.exists():
            return ref_code



class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.session.session_key, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.session.session_key,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.session.session_key,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.session.session_key, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.session.session_key,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if self.is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.session.session_key,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.session.session_key,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if self.is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.session.session_key,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "Aun no tienes una orden activa")
            return redirect("core:order-summary")
    
    def add_to_cart(request, slug, quantity):
        item = get_object_or_404(Item, slug=slug)
        try:
            stock = item.stockQuantity
            if(quantity < stock):
                if request.session.session_key == None:
                    request.session.create()
                    request.session.set_expiry(150)
                order_item, created = OrderItem.objects.get_or_create(
                    item=item,
                    user=request.session.session_key,
                    ordered=False
                )
                order_qs = Order.objects.filter(user=request.session.session_key, ordered=False)
                if order_qs.exists():
                    order = order_qs[0]
                    # check if the order item is in the order
                    if order.items.filter(item__slug=item.slug).exists():
                        order_item.quantity += quantity
                        order_item.save()
                        return redirect("core:order-summary")
                    else:
                        order_item.quantity = quantity
                        order_item.save()
                        order.items.add(order_item)
                        return redirect("core:order-summary")
                else:
                    order_item.quantity = quantity
                    ordered_date = timezone.now()
                    order = Order.objects.create(
                        user=request.session.session_key, ref_code=create_ref_code(), ordered_date=ordered_date)
                    order_item.save()
                    order.items.add(order_item)
                    return redirect("core:order-summary")
            elif (item.stockQuantity == 0):
                messages.info(request, "Este producto se acaba de agotar")
                return redirect("core:product", slug=slug)
            else:
                messages.info(request, "No hay en existencia la cantidad seleccionada")
                return redirect("core:product", slug=slug)
        except:
            print('exc')
            messages.info(request, "No hay en existencia la cantidad seleccionada")
            return redirect("core:product", slug=slug)


    def is_valid_form(self, values):
        valid = True
        for field in values:
            if field == '':
                valid = False
        return valid
