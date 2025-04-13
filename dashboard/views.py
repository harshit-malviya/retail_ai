from django.shortcuts import render
from billing.models import Sale, DailySale
from products.models import Product
from django.db.models import Sum
from datetime import date, timedelta
from django.db.models.functions import TruncDate
import json
from django.db.models import Sum, F
from django.utils.timezone import now
from datetime import timedelta

def home(request):
    view_type = request.GET.get('view', 'monthly')
    today = date.today()

    # ---------------------
    # 📈 Sales Over Time Chart (from Sale model)
    # ---------------------
    if view_type == 'daily':
        sales = Sale.objects.annotate(day=TruncDate('date'))\
            .values('day')\
            .annotate(total=Sum('total_amount'))\
            .order_by('day')
        labels = [entry['day'].strftime('%Y-%m-%d') for entry in sales]
        data = [float(entry['total']) for entry in sales]
        label_text = "Daily Sales"
    else:  # Monthly
        sales = Sale.objects.extra(select={'month': "strftime('%%Y-%%m', date)"})\
            .values('month')\
            .annotate(total=Sum('total_amount'))\
            .order_by('month')
        labels = [entry['month'] for entry in sales]
        data = [float(entry['total']) for entry in sales]
        label_text = "Monthly Sales"

    # ---------------------
    # 💰 Today’s Revenue (from DailySale)
    # ---------------------
    today_sale = DailySale.objects.filter(date=today).first()
    today_revenue = float(today_sale.total_amount) if today_sale else 0

    # ---------------------
    # 📊 Revenue Last 7 Days (from DailySale)
    # ---------------------
    last_7_days = DailySale.objects.filter(date__gte=today - timedelta(days=6)).order_by('date')
    history_labels = [entry.date.strftime('%Y-%m-%d') for entry in last_7_days]
    history_data = [float(entry.total_amount) for entry in last_7_days]

    low_stock_products = Product.objects.filter(stock_quantity__lt=F('low_stock_threshold'))

    # Slow-moving logic
    days_threshold = int(request.GET.get('slow_days', 30))  # default = 30 days
    cutoff_date = now().date() - timedelta(days=days_threshold)

    # Get IDs of products that have been sold in the last X days
    recently_sold_product_ids = Sale.objects.filter(date__gte=cutoff_date).values_list('items__id', flat=True).distinct()

    # Products NOT sold in X days
    slow_days_options = [7, 15, 30, 60, 90]
    slow_moving_products = Product.objects.exclude(saleitem__in=recently_sold_product_ids)

    return render(request, 'home.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'label_text': label_text,
        'today_revenue': today_revenue,
        'history_labels': json.dumps(history_labels),
        'history_data': json.dumps(history_data),
        'low_stock_products': low_stock_products,
        'slow_moving_products': slow_moving_products,
        'days_threshold': days_threshold,
        'slow_days_options': slow_days_options,
    })
