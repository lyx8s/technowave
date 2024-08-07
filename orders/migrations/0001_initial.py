# Generated by Django 5.0.6 on 2024-06-08 08:37

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_remove_product_polymorphic_ctype_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Номер заказа')),
                ('status', models.CharField(choices=[('PROCCESING', 'В обработке'), ('SENT', 'Отправлен'), ('DELIVERED', 'Доставлен')], default='В обработке')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая стоимость')),
                ('shipping_address', models.TextField(verbose_name='Адрес доставки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление заказа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'orders',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
                'db_table': 'ordersItems',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='orders.OrderItem', to='products.product'),
        ),
    ]
