# Generated by Django 5.1.1 on 2024-10-28 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoThanhPham', '0010_remove_order_tong_tien'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tong_tien',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
