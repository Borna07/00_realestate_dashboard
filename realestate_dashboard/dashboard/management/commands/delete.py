from django.core.management.base import BaseCommand
from dashboard.models import SaleDataset, SaleDataEntry, RentDataset, RentDataEntry

class Command(BaseCommand):
    help = 'Deletes all entries in specified models'

    def handle(self, *args, **kwargs):
        # List of models to clear
        models = [SaleDataset, SaleDataEntry, RentDataset, RentDataEntry]

        for model in models:
            model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all entries in {model.__name__}'))

