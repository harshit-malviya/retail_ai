from django import forms
from .models import Sale, SaleItem

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer']

SaleItemFormSet = forms.inlineformset_factory(
    Sale,
    SaleItem,
    fields=['product', 'quantity', 'price'],
    extra=1,
    can_delete=True
)
