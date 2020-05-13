from core.models import Order
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        Order.objects.filter(ordered=False).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted Orders'))