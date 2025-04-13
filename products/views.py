from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Product, ProductCategory
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models import F, Value
from django.db.models.functions import Lower, Replace
from django.urls import reverse

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
        return redirect('products:category_list')
    return render(request, 'products/category_form.html', {'form': form})

# CATEGORY: Edit
def category_edit(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('products:category_list')
    return render(request, 'products/category_form.html', {'form': form})

# CATEGORY: Delete
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    previous_url = request.META.get('HTTP_REFERER', reverse('products:category_list'))
    if request.method == 'POST':
        category.delete()
        return redirect('products:category_list')
    return render(request, 'products/confirm_delete.html', {'object': category, 'type': 'Category', 'cancel_url': previous_url})

# CATEGORY: Search
def category_list(request):
    query = request.GET.get('q')
    categories = ProductCategory.objects.all()
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, 'products/category_list.html', {'categories': categories, 'query': query})


# Product Views
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('products:product_list')
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})

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
        return redirect('products:product_list')
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product'})

# PRODUCT: Delete
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    previous_url = request.META.get('HTTP_REFERER', reverse('products:product_list'))
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/confirm_delete.html', {'object': product, 'type': 'Product', 'cancel_url': previous_url})

# PRODUCT: Search
def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all()

    if query:
        # Normalize: remove hyphens from both query and product name
        normalized_query = query.lower().replace('-', '').replace(' ', '')

        products = products.annotate(
            clean_name=Replace(Lower(F('name')), Value('-'), Value(''))
        ).annotate(
            clean_name=Replace(F('clean_name'), Value(' '), Value(''))
        ).filter(clean_name__icontains=normalized_query)

    return render(request, 'products/product_list.html', {'products': products, 'query': query})
