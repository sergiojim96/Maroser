from django.contrib.sessions.models import Session
from django.shortcuts import reverse
from django.conf import settings
from django.db import models
from .Item import Item

class OrderItem(models.Model):
    user = models.CharField(max_length=40)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
    def get_remove_single_item_from_cart_url(self):
        return reverse("core:remove-single-item-from-cart", kwargs={
            'slug' : self.item.slug
            })