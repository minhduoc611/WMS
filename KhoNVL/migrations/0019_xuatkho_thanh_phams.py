# Generated by Django 5.1.1 on 2024-10-23 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0018_remove_xuatkho_thanh_pham'),
    ]

    operations = [
        migrations.AddField(
            model_name='xuatkho',
            name='thanh_phams',
            field=models.ManyToManyField(to='KhoNVL.thanhpham'),
        ),
    ]
