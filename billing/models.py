from django.db import models
from customers.models import Customer
from products.models import Product

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sale #{self.id} - {self.customer.name} - ₹{self.total_amount}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Selling price at time of sale

    def get_total_price(self):
        return self.quantity * self.price

class DailySale(models.Model):
    date = models.DateField(unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.date} - ₹{self.total_amount}"
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sale, DailySale
from django.db.models import Sum
from django.utils.timezone import localdate

@receiver(post_save, sender=Sale)
def update_daily_sale(sender, instance, **kwargs):
    today = localdate(instance.date)  # handle timezone-aware datetimes
    total = Sale.objects.filter(date__date=today).aggregate(total=Sum('total_amount'))['total'] or 0
    DailySale.objects.update_or_create(
        date=today,
        defaults={'total_amount': total}
    )
