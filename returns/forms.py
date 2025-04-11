from django import forms
from .models import ProductReturn
from .models import ProductReturn, SaleItem
from django.http import JsonResponse
from billing.models import SaleItem


class ProductReturnForm(forms.ModelForm):
    class Meta:
        model = ProductReturn
        fields = ['sale', 'item', 'quantity', 'reason', 'refund_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = SaleItem.objects.none()

        if 'sale' in self.data:
            try:
                sale_id = int(self.data.get('sale'))
                self.fields['item'].queryset = SaleItem.objects.filter(sale_id=sale_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['item'].queryset = self.instance.sale.items.all()