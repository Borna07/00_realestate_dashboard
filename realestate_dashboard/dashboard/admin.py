from django.contrib import admin
from .models import City, SaleDataset, SaleDataEntry, RentDataset, RentDataEntry

# Register your models here.

admin.site.register(City)
admin.site.register(SaleDataset)
admin.site.register(SaleDataEntry)
admin.site.register(RentDataset)
admin.site.register(RentDataEntry)