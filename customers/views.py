# Create your views here.
from django.shortcuts import render
from .models import Customer
from django.core.paginator import Paginator

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
