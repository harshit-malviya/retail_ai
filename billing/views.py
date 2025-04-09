from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import SaleForm, SaleItemFormSet
from django.db import transaction

def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                sale = form.save(commit=False)
                sale.total_amount = 0  # Will calculate from items
                sale.save()

                formset.instance = sale
                items = formset.save()

                total = 0
                for item in items:
                    total += item.get_total_price()

                    # Update stock
                    item.product.stock_quantity -= item.quantity
                    item.product.save()

                sale.total_amount = total
                sale.save()

                return redirect('billing:sale_detail', sale.id)  # You'll implement this view next

    else:
        form = SaleForm()
        formset = SaleItemFormSet()
    return render(request, 'billing/create_sale.html', {'form': form, 'formset': formset})

from django.shortcuts import render, get_object_or_404
from .models import Sale

def sale_detail(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'billing/sale_detail.html', {'sale': sale})

from django.http import JsonResponse
from products.models import Product

def get_product_info(request):
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'price': float(product.selling_price),
            'stock': product.stock_quantity,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

from django.shortcuts import render, get_object_or_404
from customers.models import Customer
from .models import Sale

def customer_purchase_history(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    purchases = Sale.objects.filter(customer=customer).order_by('-date')
    return render(request, 'billing/purchase_history.html', {
        'customer': customer,
        'purchases': purchases
    })
