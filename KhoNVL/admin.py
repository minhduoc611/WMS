from django.contrib import admin
from .models import NCCVai, NVL, Order, OrderItem, ThanhPham, ThanhPhamNVL


@admin.register(NCCVai)
class NCCVaiAdmin(admin.ModelAdmin):
    list_display = ('id_ncc', 'ten_ncc', 'so_dien_thoai', 'facebook', 'website', 'dia_chi')
    search_fields = ('id_ncc', 'ten_ncc')


@admin.register(NVL)
class NVLAdmin(admin.ModelAdmin):
    list_display = ('id_vai', 'ten_vai', 'mau_sac', 'nha_cung_cap', 'so_luong_ton', 'gia')
    search_fields = ('id_vai', 'ten_vai')
    list_filter = ('nha_cung_cap',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'ngay_dat_hang',)
    search_fields = ('id',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'nvl', 'so_luong')
    search_fields = ('order__id', 'nvl__ten_vai')




@admin.register(ThanhPham)
class ThanhPhamAdmin(admin.ModelAdmin):
    list_display = ('id_thanh_pham', 'ten_thanh_pham', 'mau_sac', 'size')
    search_fields = ('id_thanh_pham', 'ten_thanh_pham')


@admin.register(ThanhPhamNVL)
class ThanhPhamNVLAdmin(admin.ModelAdmin):
    list_display = ('thanh_pham', 'nvl', 'vai_tro', 'so_luong_su_dung')
    search_fields = ('thanh_pham__ten_thanh_pham', 'nvl__ten_vai')
    list_filter = ('vai_tro',)








