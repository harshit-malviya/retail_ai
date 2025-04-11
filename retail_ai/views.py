from django.shortcuts import render
from billing.models import Sale
from django.db.models import Sum
import json
from datetime import datetime

def home(request):
    view_type = request.GET.get('view', 'monthly')

    if view_type == 'daily':
        sales = Sale.objects.extra(select={'day': "date(date)"}).values('day').annotate(total=Sum('total_amount')).order_by('day')
        labels = [entry['day'] for entry in sales]
        data = [float(entry['total']) for entry in sales]
        label_text = "Daily Sales"
    elif view_type == 'monthly':
        sales = Sale.objects.extra(select={'month': "strftime('%%Y-%%m', date)"}).values('month').annotate(total=Sum('total_amount')).order_by('month')
        labels = [entry['month'] for entry in sales]
        data = [float(entry['total']) for entry in sales]
        label_text = "Monthly Sales"

    return render(request, 'home.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'label_text': label_text
    })
