from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('create/', views.create_sale, name='create_sale'),
    path('sale/<int:sale_id>/', views.sale_detail, name='sale_detail'),
    path('api/product-info/', views.get_product_info, name='get_product_info'),


]
