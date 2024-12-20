# Generated by Django 5.1.1 on 2024-10-23 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0016_delete_tonkho'),
    ]

    operations = [
        migrations.CreateModel(
            name='XuatKho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_xuat', models.DateTimeField(auto_now_add=True)),
                ('ghi_chu', models.TextField(blank=True, null=True)),
                ('thanh_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KhoNVL.thanhpham')),
            ],
        ),
        migrations.CreateModel(
            name='XuatKhoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong_xuat', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('vai_tro', models.CharField(choices=[('Chính', 'Vải chính'), ('Lót', 'Vải lót')], max_length=10)),
                ('nvl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KhoNVL.nvl')),
                ('xuat_kho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='KhoNVL.xuatkho')),
            ],
        ),
    ]
