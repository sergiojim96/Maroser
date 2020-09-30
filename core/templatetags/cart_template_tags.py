from django import template
from core.models import Order
from core.models import Item

register = template.Library()


@register.filter
def cart_item_count(user):
    #if user.is_authenticated:
    qs = Order.objects.filter(user=user, ordered=False)
    if qs.exists():
        return qs[0].items.count()
    return 0


@register.filter
def index(indexable, i):
    return indexable[i]
