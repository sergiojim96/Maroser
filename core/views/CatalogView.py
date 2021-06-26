from django.views.generic import ListView
from ..models import Item

class CatalogView(ListView):
    queryset = Item.objects.filter(stockQuantity__gt=0) #equivalent to stockQuantity > 0
    paginate_by = 30
    template_name = "catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maybeObjects'] = filter(lambda x: x.label == 'M', Item.objects.all())
        return context

    def get(self, request, *args, **kwargs):
        self.checkSessions()
        return super().get(request, *args, **kwargs)
    
    def checkSessions(self):
        pass
