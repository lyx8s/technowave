# Generated by Django 5.0.6 on 2024-06-08 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_products_remove_shoppingcart_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='Общая стоимость'),
        ),
    ]
