from django.views.generic import ListView
from ..models import Item

class CatalogView(ListView):
    model = Item
    paginate_by = 10
    template_name = "catalog.html"