from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('create/', views.create_sale, name='create_sale'),
    path('sale/<int:sale_id>/', views.sale_detail, name='sale_detail'),
    path('api/product-info/', views.get_product_info, name='get_product_info'),
    path('history/<int:customer_id>/', views.customer_purchase_history, name='purchase_history'),
    path('history/<int:customer_id>/export/', views.export_customer_sales_excel, name='export_purchase_excel'),
    path('history/<int:customer_id>/export/pdf/', views.export_customer_sales_pdf, name='export_purchase_pdf'),
    path('api/search-customer/', views.search_customer_by_phone, name='search_customer'),

]
