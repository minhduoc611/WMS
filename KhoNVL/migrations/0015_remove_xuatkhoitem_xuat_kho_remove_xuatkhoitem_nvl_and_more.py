# Generated by Django 5.1.1 on 2024-10-23 03:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0014_nvl_gia_delete_giancc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xuatkhoitem',
            name='xuat_kho',
        ),
        migrations.RemoveField(
            model_name='xuatkhoitem',
            name='nvl',
        ),
        migrations.RemoveField(
            model_name='xuatkhoitem',
            name='vi_tri_xuat',
        ),
        migrations.RenameField(
            model_name='thanhphamnvl',
            old_name='so_luong_can',
            new_name='so_luong_su_dung',
        ),
        migrations.AddField(
            model_name='thanhphamnvl',
            name='vai_tro',
            field=models.CharField(choices=[('Chính', 'Vải chính'), ('Lót', 'Vải lót')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='thanhphamnvl',
            name='nvl',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thanhpham_nguyenlieu_khoNVL', to='KhoNVL.nvl'),
        ),
        migrations.AlterField(
            model_name='thanhphamnvl',
            name='thanh_pham',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nguyen_vat_lieu_khoNVL', to='KhoNVL.thanhpham'),
        ),
        migrations.DeleteModel(
            name='XuatKho',
        ),
        migrations.DeleteModel(
            name='XuatKhoItem',
        ),
    ]
