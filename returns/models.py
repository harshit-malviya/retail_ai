from django.db import models

# Create your models here.
from products.models import Product
from billing.models import Sale, SaleItem

class ProductReturn(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    item = models.ForeignKey(SaleItem, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reason = models.TextField(blank=True, null=True)
    return_date = models.DateTimeField(auto_now_add=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Return of {self.quantity} x {self.product.name} from Sale #{self.sale.id}"
