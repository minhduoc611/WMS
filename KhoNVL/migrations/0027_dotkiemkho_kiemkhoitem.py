# Generated by Django 5.1.1 on 2024-11-09 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0026_remove_order_ncc_remove_order_phi_van_chuyen_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DotKiemKho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_kiem', models.DateTimeField(auto_now_add=True)),
                ('ghi_chu', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KiemKhoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong_thuc_te', models.PositiveIntegerField()),
                ('so_luong_ly_thuyet', models.PositiveIntegerField()),
                ('dot_kiem_kho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='KhoNVL.dotkiemkho')),
                ('nvl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KhoNVL.nvl')),
            ],
        ),
    ]
