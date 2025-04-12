from django.contrib import admin

# Register your models here.
# billing/admin.py (or the app where you defined Sale and SaleItem)

from django.contrib import admin
from .models import Sale, SaleItem, DailySale

admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(DailySale)
