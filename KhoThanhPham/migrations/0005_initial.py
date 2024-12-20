# Generated by Django 5.1.1 on 2024-10-28 02:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('KhoNVL', '0023_thanhpham_so_luong_ton_alter_xuatkhonvl_vai_tro'),
        ('KhoThanhPham', '0004_remove_thanhphamnvl_thanh_pham_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NhapKhoThanhPham',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_nhap', models.DateTimeField(auto_now_add=True)),
                ('ghi_chu', models.TextField(blank=True, null=True)),
                ('trang_thai', models.CharField(choices=[('pending', 'Chờ duyệt'), ('approved', 'Đã duyệt'), ('rejected', 'Từ chối')], default='pending', max_length=10)),
                ('xuat_kho', models.ForeignKey(blank=True, help_text='Đơn xuất kho NVL dùng để sản xuất', null=True, on_delete=django.db.models.deletion.SET_NULL, to='KhoNVL.xuatkho')),
            ],
        ),
        migrations.CreateModel(
            name='NhapKhoThanhPhamItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong', models.PositiveIntegerField(default=0)),
                ('nhap_kho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='KhoThanhPham.nhapkhothanhpham')),
                ('thanh_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KhoNVL.thanhpham')),
            ],
        ),
    ]
