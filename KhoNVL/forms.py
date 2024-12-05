# forms.py
from django import forms
from .models import *
from django.forms import inlineformset_factory


from django import forms
from .models import OrderItem, NVL

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['nvl', 'so_luong']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

from django.forms import inlineformset_factory

OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    form=OrderItemForm,  # Sử dụng form tùy chỉnh đã tạo
    extra=1,
    can_delete=True
)



from django import forms
from .models import NVL

class NVLForm(forms.ModelForm):
    gia = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="Giá",
        required=True
    )

    class Meta:
        model = NVL
        fields = ['ten_vai', 'mau_sac', 'nha_cung_cap', 'so_luong_ton', 'don_vi_tinh', 'gia', 'hinh_anh']
        widgets = {
            'ten_vai': forms.TextInput(attrs={'class': 'form-control'}),
            'mau_sac': forms.TextInput(attrs={'class': 'form-control'}),
            'nha_cung_cap': forms.Select(attrs={'class': 'form-control'}),
            'so_luong_ton': forms.NumberInput(attrs={'class': 'form-control'}),
            'don_vi_tinh': forms.TextInput(attrs={'class': 'form-control'}),
            'gia': forms.NumberInput(attrs={'class': 'form-control'}),
            'hinh_anh': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        nvl = super().save(commit=False)
        if commit:
            nvl.save()
        return nvl




from django import forms

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()



