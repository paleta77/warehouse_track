# Generated by Django 5.1.7 on 2025-05-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
