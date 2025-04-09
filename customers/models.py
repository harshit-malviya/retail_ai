from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    visit_count = models.PositiveIntegerField(default=0)
    last_purchase_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional tagging
    TAG_CHOICES = (
        ('vip', 'VIP'),
        ('regular', 'Regular'),
        ('new', 'New'),
    )
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
