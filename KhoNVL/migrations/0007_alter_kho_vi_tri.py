# Generated by Django 5.1.1 on 2024-10-14 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0006_kho_tonkho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kho',
            name='vi_tri',
            field=models.CharField(default='A1', max_length=100),
        ),
    ]