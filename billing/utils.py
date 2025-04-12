from datetime import date
from django.db.models import Sum
from billing.models import Sale, DailySale
from django.db import IntegrityError

def calculate_daily_sale_summary(target_date=None):
    target_date = target_date or date.today()

    # Sum all sales for that day (handle datetime fields)
    sales = Sale.objects.filter(date__date=target_date)
    total = sales.aggregate(total=Sum('total_amount'))['total'] or 0

    # Create or update DailySale entry
    daily_sale, created = DailySale.objects.update_or_create(
        date=target_date,
        defaults={'total_amount': total}
    )
    return daily_sale
