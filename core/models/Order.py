from django.conf import settings
from django.db import models
from .OrderItem import OrderItem
from .UserProfile import UserProfile
from django.contrib.sessions.models import Session

class Order(models.Model):
    user = models.CharField(max_length=40)
    ref_code = models.CharField(max_length=15, blank=True, null=True, unique=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)
    
    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += round(order_item.get_final_price(), 2)
        if self.coupon:
            total -= self.coupon.amount
        total = round(total, 2)
        return total
