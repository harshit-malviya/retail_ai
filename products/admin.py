# Register your models here.
from django.contrib import admin
from .models import Product, ProductCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'size', 'color', 'cost_price', 'selling_price', 'stock_quantity')

admin.site.register(ProductCategory)
