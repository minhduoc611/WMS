# Generated by Django 5.1.1 on 2024-10-14 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KhoNVL', '0007_alter_kho_vi_tri'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tonkho',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='tonkho',
            name='vi_tri_kho',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='tonkho',
            name='kho',
        ),
    ]
