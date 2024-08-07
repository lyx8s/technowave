# Generated by Django 5.0.6 on 2024-06-09 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_total_price'),
        ('products', '0002_remove_product_polymorphic_ctype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='quantity',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Общая стоимость'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Кол-во товара')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='orders.shoppingcart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
