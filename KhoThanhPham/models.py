from django.db import models
from KhoNVL.models import ThanhPham

class NhapKhoThanhPham(models.Model):
    ngay_nhap = models.DateTimeField(auto_now_add=True)
    ghi_chu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Nhập kho #{self.id} - {self.ngay_nhap.strftime('%d/%m/%Y')}"

class NhapKhoThanhPhamItem(models.Model):
    nhap_kho = models.ForeignKey(NhapKhoThanhPham, related_name='items', on_delete=models.CASCADE)
    thanh_pham = models.ForeignKey(ThanhPham, on_delete=models.CASCADE)
    so_luong = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.so_luong} x {self.thanh_pham.ten_thanh_pham} trong nhập kho #{self.nhap_kho.id}"
    



class XuatKhoThanhPham(models.Model):
    ngay_xuat = models.DateTimeField(auto_now_add=True)
    ghi_chu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Xuất kho #{self.id} - {self.ngay_xuat.strftime('%d/%m/%Y')}"

class XuatKhoThanhPhamItem(models.Model):
    xuat_kho = models.ForeignKey(XuatKhoThanhPham, related_name='items', on_delete=models.CASCADE)
    thanh_pham = models.ForeignKey('KhoNVL.ThanhPham', on_delete=models.CASCADE) 
    so_luong = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.so_luong} x {self.thanh_pham.ten_thanh_pham} trong xuất kho #{self.xuat_kho.id}"

    

class KiemKhoThanhPham(models.Model):
    ngay_kiem = models.DateTimeField(auto_now_add=True)
    ghi_chu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Kiểm kho #{self.id} - {self.ngay_kiem.strftime('%d/%m/%Y')}"

class KiemKhoThanhPhamItem(models.Model):
    kiem_kho = models.ForeignKey(KiemKhoThanhPham, related_name='items', on_delete=models.CASCADE)
    thanh_pham = models.ForeignKey(ThanhPham, on_delete=models.CASCADE)
    so_luong_ly_thuyet = models.PositiveIntegerField() 
    so_luong_thuc_te = models.PositiveIntegerField() 
    so_luong_chenh_lech = models.IntegerField(blank=True, null=True) 

    def save(self, *args, **kwargs):
        if self.so_luong_thuc_te is not None and self.so_luong_ly_thuyet is not None:
            self.so_luong_chenh_lech = self.so_luong_thuc_te - self.so_luong_ly_thuyet
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.so_luong_thuc_te} x {self.thanh_pham.ten_thanh_pham} trong kiểm kho #{self.kiem_kho.id}"