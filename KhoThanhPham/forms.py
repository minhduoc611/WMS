from django.forms import modelformset_factory
from .models import *
from django import forms

ThanhPhamItemFormSet = modelformset_factory(
    NhapKhoThanhPhamItem,
    fields=('thanh_pham', 'so_luong'),
    extra=1,  
    can_delete=True  
)


class NhapKhoThanhPhamItemForm(forms.ModelForm):
    class Meta:
        model = NhapKhoThanhPhamItem
        fields = ['thanh_pham', 'so_luong']


XuatThanhPhamItemFormSet = modelformset_factory(
    XuatKhoThanhPhamItem,
    fields=('thanh_pham', 'so_luong'),
    extra=1,  # Số lượng form trống bổ sung
    can_delete=True
)

class XuatKhoThanhPhamItemForm(forms.ModelForm):
    class Meta:
        model = XuatKhoThanhPhamItem
        fields = ['thanh_pham', 'so_luong']