from django import forms
from .models import Customer, Order

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'status', 'interest']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الكامل'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'interest': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاهتمامات'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product_details', 'total_price', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'product_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'تفاصيل الديكور / الطلب'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ (دج)'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }