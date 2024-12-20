# Generated by Django 5.1.1 on 2024-10-20 06:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('KhoNVL', '0010_xuatkho_xuatkhoitem_delete_xuatnvl'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThanhPham',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_thanh_pham', models.CharField(blank=True, max_length=10, unique=True)),
                ('ten_thanh_pham', models.CharField(max_length=255)),
                ('mau_sac', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ThanhPhamNVL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong_can', models.PositiveIntegerField()),
                ('nvl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KhoNVL.nvl')),
                ('thanh_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nguyen_vat_lieu', to='KhoThanhPham.thanhpham')),
            ],
        ),
    ]
