# Generated by Django 5.1.2 on 2024-10-31 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodocts',
            name='Brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.brand'),
        ),
    ]