from django.db import models
from decimal import Decimal
from datetime import datetime

class NCCVai(models.Model):
    id_ncc = models.CharField(max_length=10, unique=True, blank=True)
    ten_ncc = models.CharField(max_length=255)
    so_dien_thoai = models.CharField(max_length=15, null=True, blank=True)
    facebook = models.URLField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    dia_chi = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id_ncc:
            last_ncc = NCCVai.objects.all().order_by('id_ncc').last()
            if last_ncc:
                last_id = last_ncc.id_ncc[-3:]
                new_id = int(last_id) + 1
                self.id_ncc = f'SVU{new_id:03d}'
            else:
                self.id_ncc = 'SVU000'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id_ncc} - {self.ten_ncc}'


class NVL(models.Model):
    id_vai = models.CharField(max_length=10, unique=True, blank=True)
    hinh_anh = models.ImageField(upload_to='nvl_images/', null=True, blank=True)
    ten_vai = models.CharField(max_length=255)
    don_vi_tinh = models.CharField(max_length=50)
    mau_sac = models.CharField(max_length=50)
    nha_cung_cap = models.ForeignKey(NCCVai, on_delete=models.CASCADE)
    so_luong_ton = models.PositiveIntegerField(default=0)
    gia = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Thêm trường giá

    def save(self, *args, **kwargs):
        if not self.id_vai:
            last_nvl = NVL.objects.all().order_by('id').last()
            if last_nvl:
                last_id = last_nvl.id_vai[3:]
                last_num = int(last_id)
                new_id = f'MAV{last_num + 1:03d}'
            else:
                new_id = 'MAV001'
            self.id_vai = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id_vai} - {self.ten_vai} ({self.nha_cung_cap.ten_ncc}) - Màu: {self.mau_sac} - Giá: {self.gia}'


class Order(models.Model):
    ngay_dat_hang = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - Ngày: {self.ngay_dat_hang.strftime("%d/%m/%Y")}'

    def tong_gia_tri(self):
        # Tính tổng giá trị của các mặt hàng trong đơn hàng
        tong_tien_hang = sum(item.so_luong * item.get_gia() for item in self.items.all())
        return tong_tien_hang


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    nvl = models.ForeignKey(NVL, on_delete=models.CASCADE)
    so_luong = models.PositiveIntegerField()

    def get_gia(self):
        return self.nvl.gia

    def get_total(self):
        return self.so_luong * self.get_gia()

    def __str__(self):
        return f'{self.so_luong} x {self.nvl.ten_vai} trong Order #{self.order.id}'



class ThanhPham(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    id_thanh_pham = models.CharField(max_length=10, unique=True, blank=True)
    ten_thanh_pham = models.CharField(max_length=255)
    mau_sac = models.CharField(max_length=50)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    so_luong_ton = models.PositiveIntegerField(default=0)
    don_gia = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Thêm trường đơn giá

    def save(self, *args, **kwargs):
        if not self.id_thanh_pham:
            last_thanh_pham = ThanhPham.objects.all().order_by('id').last()
            if last_thanh_pham:
                last_id = last_thanh_pham.id_thanh_pham[-3:]
                new_id = int(last_id) + 1
                self.id_thanh_pham = f'THP{new_id:03d}'
            else:
                self.id_thanh_pham = 'THP001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ten_thanh_pham} - {self.mau_sac} - {self.size} - Giá: {self.don_gia} VND'


class ThanhPhamNVL(models.Model):
    VAITRO_CHOICES = [
        ('Vải Chính', 'Vải chính'),
        ('Vải Lót', 'Vải lót'),
    ]

    thanh_pham = models.ForeignKey(ThanhPham, related_name='nguyen_vat_lieu_khoNVL', on_delete=models.CASCADE)
    nvl = models.ForeignKey(NVL, related_name='thanhpham_nguyenlieu_khoNVL', on_delete=models.CASCADE)
    vai_tro = models.CharField(max_length=10, choices=VAITRO_CHOICES)
    so_luong_su_dung = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.nvl.ten_vai} - {self.vai_tro} cho {self.thanh_pham.ten_thanh_pham}'


class DotXuatKho(models.Model):
    ngay_xuat = models.DateTimeField(auto_now_add=True)
    ghi_chu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Đợt xuất kho #{self.id} - {self.ngay_xuat.strftime('%d/%m/%Y')}"

class XuatKhoItem(models.Model):
    dot_xuat_kho = models.ForeignKey(DotXuatKho, related_name='items', on_delete=models.CASCADE)
    nvl = models.ForeignKey(NVL, on_delete=models.CASCADE)
    so_luong_xuat = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
       

    def __str__(self):
        return f"{self.so_luong_xuat} x {self.nvl.ten_vai} trong đợt xuất kho #{self.dot_xuat_kho.id}"


class DotKiemKho(models.Model):
    ngay_kiem = models.DateTimeField(auto_now_add=True)
    ghi_chu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Đợt kiểm kho #{self.id} - {self.ngay_kiem.strftime('%d/%m/%Y')}"

class KiemKhoItem(models.Model):
    dot_kiem_kho = models.ForeignKey(DotKiemKho, related_name='items', on_delete=models.CASCADE)
    nvl = models.ForeignKey(NVL, on_delete=models.CASCADE)
    so_luong_thuc_te = models.PositiveIntegerField()
    so_luong_ly_thuyet = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.so_luong_ly_thuyet:
            self.so_luong_ly_thuyet = self.nvl.so_luong_ton
        super().save(*args, **kwargs)

    def chenh_lech(self):
        return self.so_luong_thuc_te - self.so_luong_ly_thuyet

    def __str__(self):
        return f"{self.nvl.ten_vai} trong Đợt kiểm kho #{self.dot_kiem_kho.id}"
