from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('ncc/', views.ncc_list, name='ncc-list'),
    path('ncc/<int:id>/delete/', views.ncc_delete, name='ncc_delete'),
    path('ncc/<int:id>/edit/', views.ncc_edit, name='ncc_edit'),
    path('', views.index, name='index'),
    path('ncc/add/', views.add_ncc, name='add_ncc'),
    path('nvl/', views.nvl_list, name='nvl-list'),
    path('tao_don_hang/', views.tao_don_hang, name='tao_don_hang'),
    path('danh_sach_don_nhap_kho/', views.danh_sach_don_nhap_kho, name='danh_sach_don_nhap_kho'),
    path('chi-tiet-don-nhap-kho/<int:order_id>/', chi_tiet_don_nhap_kho, name='chi_tiet_don_nhap_kho'),
    path('upload_excel_NCC_view/',upload_excel_NCC_view, name='upload_excel_NCC_view'),
    path('add_nvl/', views.add_nvl, name='add_nvl'),
    path('upload_excel_nvl/', views.upload_excel_nvl, name='upload_excel_nvl'),
    path('tao-dot-kiem-kho/', tao_dot_kiem_kho, name='tao_dot_kiem_kho'),
    path('chi-tiet-dot-kiem-kho/<int:pk>/', chi_tiet_dot_kiem_kho, name='chi_tiet_dot_kiem_kho'),
    path('luu-dot-kiem-kho/', views.luu_dot_kiem_kho, name='luu_dot_kiem_kho'),
    path('danh-sach-dot-kiem-kho/', views.danh_sach_dot_kiem_kho, name='danh_sach_dot_kiem_kho'),
    path('tao-dot-xuat-kho/', views.tao_dot_xuat_kho, name='tao_dot_xuat_kho'),
    path('danh-sach-dot-xuat-kho/', danh_sach_dot_xuat_kho, name='danh_sach_dot_xuat_kho'),
    path('chi-tiet-dot-xuat-kho/<int:pk>/', chi_tiet_dot_xuat_kho, name='chi_tiet_dot_xuat_kho'),
    path('dashboard/', views.tableau_dashboard, name='tableau_dashboard'),


]
