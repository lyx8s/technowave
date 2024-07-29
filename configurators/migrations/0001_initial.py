# Generated by Django 5.0.6 on 2024-06-10 12:59

import django.db.models.deletion
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
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Конфигуратор',
                'verbose_name_plural': 'Конфигураторы',
                'db_table': 'configuration',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('component', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configuration_components', to='configurators.configuration')),
            ],
            options={
                'verbose_name': 'Компонент',
                'verbose_name_plural': 'Компоненты',
                'db_table': 'component',
            },
        ),
    ]