from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'order_type', 'address', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'}),
            'order_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Delivery address (leave blank for pickup)'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Any special instructions (optional)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')
        address = cleaned_data.get('address')
        if order_type == 'DELIVERY' and not address:
            self.add_error('address', 'Address is required for home delivery.')
        return cleaned_data
