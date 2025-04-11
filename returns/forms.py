from django import forms
from .models import ProductReturn

class ProductReturnForm(forms.ModelForm):
    class Meta:
        model = ProductReturn
        fields = ['sale', 'item', 'product', 'quantity', 'reason', 'refund_amount']
