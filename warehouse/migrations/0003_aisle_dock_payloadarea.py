# Generated by Django 5.1.7 on 2025-03-18 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_warehouse_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aisle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('length', models.IntegerField()),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Dock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='PayloadArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('payload_type', models.CharField(choices=[('food', 'Food'), ('drinks', 'Drinks'), ('rtv', 'RTV'), ('agd', 'AGD'), ('electronics', 'Electronics'), ('other', 'Other')], default='other', max_length=50)),
                ('aisle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.aisle')),
            ],
        ),
    ]
