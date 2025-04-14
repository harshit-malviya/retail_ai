# Create your views here.
from django.shortcuts import render
from .models import Customer
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm
from django.contrib import messages
from accounts.decorators import admin_required


def customer_list(request):
    query = request.GET.get('q')
    customers = Customer.objects.filter(is_active=True)

    if query:
        customers = customers.filter(
            name__icontains=query
        ) | customers.filter(
            phone__icontains=query
        )

    paginator = Paginator(customers.order_by('-updated_at'), 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customers/customer_list.html', {
        'page_obj': page_obj,
        'query': query,
    })

# Add Customer
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add Customer'})

# Edit Customer
@admin_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Edit Customer'})

# Delete Customer (soft delete)
@admin_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.is_active = False
    customer.save()
    messages.warning(request, 'Customer deleted (soft delete).')
    return redirect('customers:customer_list')
