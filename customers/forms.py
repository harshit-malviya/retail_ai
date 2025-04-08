# customers/forms.py

from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'city', 'state', 'pincode', 'tag', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }
