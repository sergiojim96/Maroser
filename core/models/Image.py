from django.utils.html import format_html
from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='ItemImage/')

    def __str__(self):
        html = '<a href="{url}" target="_blank"><img src="{url}" width="150" height="150"/></a>'
        return format_html(''.join(html.format(url=self.image.url)))