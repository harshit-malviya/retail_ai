from django.urls import path
from . import views

app_name = 'returns'

urlpatterns = [
    path('return/', views.return_product, name='return_product'),
    path('success/', views.return_success, name='success'),
    path('ajax/load-sale-items/', views.load_sale_items, name='ajax_load_sale_items'),
]
