from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ProductReturnForm
from .utils import process_return
from django.http import HttpResponse
from django.http import JsonResponse
from billing.models import SaleItem

def return_product(request):
    if request.method == 'POST':
        form = ProductReturnForm(request.POST)
        if form.is_valid():
            return_obj = form.save(commit=False)
            return_obj.product = return_obj.item.product  # Auto-set product from item
            return_obj.save()
            process_return(return_obj)
            return redirect('returns:success')
    else:
        form = ProductReturnForm()
    return render(request, 'returns/return_form.html', {'form': form})

def return_success(request):
    return render(request, 'returns/return_success.html')
    return HttpResponse("Product return successful and invoice updated.")

def load_sale_items(request):
    sale_id = request.GET.get('sale_id')
    items = SaleItem.objects.filter(sale_id=sale_id).select_related('product')
    data = [
        {
            'id': item.id,
            'product': item.product.name,
            'quantity': item.quantity,
        }
        for item in items
    ]
    return JsonResponse(data, safe=False)
