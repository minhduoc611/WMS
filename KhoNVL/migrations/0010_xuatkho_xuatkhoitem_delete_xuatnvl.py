# Generated by Django 5.1.1 on 2024-10-14 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0009_xuatnvl'),
    ]

    operations = [
        migrations.CreateModel(
            name='XuatKho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_xuat', models.DateTimeField(auto_now_add=True)),
                ('ghi_chu', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='XuatKhoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong_xuat', models.PositiveIntegerField()),
                ('nvl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KhoNVL.nvl')),
                ('vi_tri_xuat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KhoNVL.tonkho')),
                ('xuat_kho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='KhoNVL.xuatkho')),
            ],
        ),
        migrations.DeleteModel(
            name='XuatNVL',
        ),
    ]
