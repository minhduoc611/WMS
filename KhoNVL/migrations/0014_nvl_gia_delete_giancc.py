# Generated by Django 5.1.1 on 2024-10-22 06:18

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0013_nvl_so_luong_ton'),
    ]

    operations = [
        migrations.AddField(
            model_name='nvl',
            name='gia',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.DeleteModel(
            name='GiaNCC',
        ),
    ]
