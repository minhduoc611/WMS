# Generated by Django 5.1.1 on 2024-10-28 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0023_thanhpham_so_luong_ton_alter_xuatkhonvl_vai_tro'),
    ]

    operations = [
        migrations.AddField(
            model_name='thanhpham',
            name='don_gia',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
