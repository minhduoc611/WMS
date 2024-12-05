from django.urls import path
from . import views
from .views import *



app_name = 'KhoThanhPham'


urlpatterns = [
     path('tao-nhap-kho-thanh-pham/', views.nhap_kho_thanh_pham, name='tao_nhap_kho_thanh_pham'),
     path('danh_sach_nhap_kho/', views.danh_sach_don_nhap_kho, name='danh_sach_nhap_kho'),
     path('chi-tiet-nhap-kho/<int:pk>/', views.chi_tiet_don_nhap_kho, name='chi_tiet_don_nhap_kho'),
     path('danh-sach-thanh-pham/', danh_sach_thanh_pham, name='danh_sach_thanh_pham'),
     path('xuat-kho-thanh-pham/', xuat_kho_thanh_pham, name='xuat_kho_thanh_pham'),
     path('danh-sach-xuat-kho/', views.danh_sach_xuat_kho_thanh_pham, name='danh_sach_xuat_kho_thanh_pham'),
     path('chi-tiet-don-xuat-kho/<int:pk>/', views.chi_tiet_don_xuat_kho_thanh_pham, name='chi_tiet_don_xuat_kho_thanh_pham'),
     path('tao-dot-kiem-kho-thanh-pham/', views.tao_dot_kiem_kho_thanh_pham, name='tao_dot_kiem_kho_thanh_pham'),
     path('luu-dot-kiem-kho-thanh-pham/', views.luu_dot_kiem_kho_thanh_pham, name='luu_dot_kiem_kho_thanh_pham'),
     path('chi-tiet-dot-kiem-kho-thanh-pham/<int:pk>/', views.chi_tiet_dot_kiem_kho_thanh_pham, name='chi_tiet_dot_kiem_kho_thanh_pham'),
     path('danh-sach-dot-kiem-kho-thanh-pham/', views.danh_sach_dot_kiem_kho_thanh_pham, name='danh_sach_dot_kiem_kho_thanh_pham'),
     path('add-thanh-pham/', add_thanh_pham, name='add_thanh_pham'),
     path('upload_excel/', views.upload_excel, name='upload_excel'),
     
]

