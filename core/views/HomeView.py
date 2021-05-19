from django.http.response import JsonResponse
from django.views.generic import ListView
from django.core.mail import EmailMessage
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

    def send_mail(request):
        try:
            if request.is_ajax() and request.method == "GET":
                mail = request.GET.get("mail")
                email = EmailMessage(
                'SashaCollections contacto', HomeView.getMailMessage(), "sashacollectioncr@gmail.com", [mail])
                email.send()
                return JsonResponse({"scc": "true"}, status=200)
            else:
                return JsonResponse({"scc": "false"}, status=400)
        except:
            return JsonResponse({"scc": "false"}, status=400)
    
    def getMailMessage():
        message = f'''Hola!
Gracias por confiar en nosotros y ponerte en contacto.
¿Cómo podemos ayudarte?'''
        return message

