# Generated by Django 5.0.6 on 2024-06-06 18:27

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Заголовок атрибута')),
                ('name', models.CharField(help_text='Тип матрицы:', max_length=100, verbose_name='Наименование атрибута')),
            ],
            options={
                'verbose_name': 'Атрибут товара',
                'verbose_name_plural': 'Атрибуты товаров',
                'db_table': 'attribute',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(editable=False, max_length=75, unique=True)),
                ('image', models.FileField(upload_to='pictures/categories/images', validators=[django.core.validators.FileExtensionValidator(['svg'])])),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'categories',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=30, verbose_name='Производитель')),
                ('model_name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Наименование модели')),
                ('display_name', models.CharField(max_length=100, verbose_name='Наименование товара')),
                ('code_model', models.CharField(max_length=10, unique=True, verbose_name='Код товара')),
                ('article_number', models.CharField(max_length=15, unique=True, verbose_name='Артикул')),
                ('description', models.CharField(max_length=200, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена товара')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/images/', verbose_name='Изображения товара')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(help_text='OLED', verbose_name='Значение атрибута')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.attribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_product', to='products.product')),
            ],
            options={
                'verbose_name': 'Атрибут продукта',
                'verbose_name_plural': 'Атрибуты продуктов',
                'db_table': 'product_attribute',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(related_name='in_attribute', through='products.ProductAttribute', to='products.attribute'),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(editable=False, max_length=75, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='pictures/subcategories/images', verbose_name='Иконка подкатегории')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_category', to='products.category')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
                'db_table': 'subcategories',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_subcategory', to='products.subcategory', verbose_name='Категория товара'),
        ),
    ]
