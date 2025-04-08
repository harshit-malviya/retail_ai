from django.urls import path
from . import views

urlpatterns = [
    path('products/create/', views.product_create, name='product_create'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

]
