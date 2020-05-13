from django.views.generic import DetailView
from ..models import Item

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"