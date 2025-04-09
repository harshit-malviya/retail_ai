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

import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from customers.models import Customer
from .models import Sale

def export_customer_sales_excel(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    sales = Sale.objects.filter(customer=customer).order_by('-date')

    # Create workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Purchase History"

    # Header
    headers = ['Invoice ID', 'Date', 'Total Amount (₹)']
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        ws[f'{col_letter}1'] = header

    # Data rows
    for row_num, sale in enumerate(sales, 2):
        ws[f'A{row_num}'] = sale.id
        ws[f'B{row_num}'] = sale.date.strftime('%Y-%m-%d %H:%M')
        ws[f'C{row_num}'] = float(sale.total_amount)

    # Set content type and response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"{customer.name.replace(' ', '_')}_Purchase_History.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'

    wb.save(response)
    return response

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def export_customer_sales_pdf(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    sales = Sale.objects.filter(customer=customer).order_by('-date')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, f"Purchase History for {customer.name}")
    y -= 30

    p.setFont("Helvetica", 10)
    p.drawString(50, y, "Invoice ID")
    p.drawString(150, y, "Date")
    p.drawString(300, y, "Total Amount (₹)")
    y -= 20

    for sale in sales:
        if y < 50:
            p.showPage()
            y = height - 50

        p.drawString(50, y, str(sale.id))
        p.drawString(150, y, sale.date.strftime('%Y-%m-%d %H:%M'))
        p.drawString(300, y, f"{sale.total_amount:.2f}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"{customer.name.replace(' ', '_')}_Purchase_History.pdf"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
