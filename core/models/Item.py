from django.shortcuts import reverse
from django.db import models

CATEGORY_CHOICES = (
    ('M', 'Mujer'),
    ('H', 'Hombre'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('M', 'maybe'),  # juguetes que pueden interesar
    ('B', 'bSeller')  # juguetes bestSeller cambiar apenas pueda
 )

class Item(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    long_description = models.TextField(blank=True, null=True)
    image = models.ImageField()
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)
    largeImage = models.ImageField(blank=True, null=True)
    footerImage = models.ImageField(blank = True, null = True)
    footerImage2 = models.ImageField(blank = True, null = True)
    footerImage3 = models.ImageField(blank = True, null = True)
    stockQuantity = models.IntegerField(default=1)
    sales = models.IntegerField(default=0)
    smart = models.BooleanField(default=False)



    def __str__(self):
        return self.title


    def get_smart(self):
        return self.smart


    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart-slug", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:async-remove-from-cart", kwargs={
            'slug': self.slug
        })

    def image_generator(self):
        pass

    def is_available(self, quantity):
        if(self.stockQuantity >= quantity):
            self.decreaseStock(quantity)
            return True
        return False

    # when byuing
    def decreaseStock(self, quantity):
        self.stockQuantity -= quantity
        self.save(update_fields=['stockQuantity'])
    
    def get_dollar_price(self):
        return f"${self.price}"


    #def increaseUnreserved(self, quantity):
     #   self.unreservedQuantity += quantity
     #   self.save(update_fields=['unreservedQuantity'])
