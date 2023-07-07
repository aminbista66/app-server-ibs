# Generated by Django 4.2.1 on 2023-07-05 08:01

from django.db import migrations, models
import django.db.models.deletion
import fiscalyear.utils
import order.validator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('room', '0001_initial'),
        ('companyinfo', '0001_initial'),
        ('table', '0001_initial'),
        ('customer', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_year', models.CharField(max_length=10, validators=[fiscalyear.utils.validate_fiscal_year])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='companyinfo.companyinfo')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='customer.customer')),
                ('products', models.ManyToManyField(to='product.product')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='table_orders', to='table.table')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_year', models.CharField(max_length=10, validators=[fiscalyear.utils.validate_fiscal_year])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField(validators=[order.validator.validate_minimum])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('cancelled', 'Cancelled'), ('issued', 'Issued')], default='issued', max_length=64)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='companyinfo.companyinfo')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='room_orders', to='customer.customer')),
                ('products', models.ManyToManyField(to='product.product')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='room_orders', to='room.bookedroom')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]