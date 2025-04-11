from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ProductReturnForm
from .utils import process_return
from django.http import HttpResponse

def return_product(request):
    if request.method == 'POST':
        form = ProductReturnForm(request.POST)
        if form.is_valid():
            return_obj = form.save()
            process_return(return_obj)
            return redirect('returns:success')
    else:
        form = ProductReturnForm()
    return render(request, 'returns/return_form.html', {'form': form})

def return_product(request):
    if request.method == 'POST':
        form = ProductReturnForm(request.POST)
        if form.is_valid():
            return_obj = form.save()
            process_return(return_obj)
            return redirect('returns:success')
    else:
        form = ProductReturnForm()
    return render(request, 'returns/return_form.html', {'form': form})

def return_success(request):
    return HttpResponse("Product return successful and invoice updated.")
