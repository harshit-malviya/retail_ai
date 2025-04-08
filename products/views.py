from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Product, ProductCategory
from django import forms
from django.shortcuts import get_object_or_404



# Forms
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']

# Category Views
def category_list(request):
    categories = ProductCategory.objects.all()
    # print(categories)
    return render(request, 'products/category_list.html', {'categories': categories})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'products/category_form.html', {'form': form})

# CATEGORY: Edit
def category_edit(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'products/category_form.html', {'form': form})

# CATEGORY: Delete
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'products/confirm_delete.html', {'object': category, 'type': 'Category'})



# Product Views
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/product_form.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    # print(products)
    return render(request, 'products/product_list.html', {'products': products})

# PRODUCT: Edit
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/product_form.html', {'form': form})

# PRODUCT: Delete
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {'object': product, 'type': 'Product'})


