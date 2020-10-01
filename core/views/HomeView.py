from django.views.generic import ListView
from ..models import Item

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"

    def fudfd(self, item):
        if item.label == 'B':
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = 0
        context['best_seller_c'] = filter(self.fudfd, Item.objects.all())
        return context

