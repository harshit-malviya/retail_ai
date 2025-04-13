# customers/forms.py

from django import forms
from .models import Customer
from django.core.exceptions import ValidationError

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'city', 'state', 'pincode', 'tag', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    # customers/forms.py

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')

        if phone and email:
            # Check for existing customers excluding the current one (self.instance)
            qs = Customer.objects.filter(phone=phone, email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError("A customer with this phone and email already exists.")
