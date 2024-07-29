from datetime import datetime

from django.db import models
from django.utils.text import slugify


from users.models import CustomUser
from . import category


# ------ Модели характеристик товара ------


class Attribute(models.Model):
    """
    Атрибуты товара - тип матрицы, яркость и прочее
    """
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок атрибута",
        unique=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование атрибута",
        help_text="Тип матрицы:",
    )

    class Meta:
        db_table = "attribute"
        verbose_name = 'Атрибут товара'
        verbose_name_plural = 'Атрибуты товаров'
        ordering = ('-id',)

    def get_title_data(self):
        """
        Получить все заголовки атрибутов
        """
        title = Attribute.objects.order_by('chipset').values_list('chipset',flat=True).distinct()
        return {
            'title': title
        }

    def __str__(self):
        return f'{self.title.title}: {self.name}'


class ProductAttribute(models.Model):
    """
    Атрибуты для каждого товара
    """

    product = models.ForeignKey(
        'Product',
        related_name='in_product',
        on_delete=models.CASCADE
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE
    )
    value = models.TextField(
        verbose_name="Значение атрибута",
        help_text="OLED"
    )

    class Meta:
        db_table = "product_attribute"
        verbose_name = 'Атрибут продукта'
        verbose_name_plural = 'Атрибуты продуктов'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.product}'


# ------ Модель товара ------

class Product(models.Model):
    """
    Товары в магазине
    """

    manufacturer = models.CharField(max_length=30,
                                    verbose_name="Производитель")
    model_name = models.CharField(max_length=100,
                                  null=True,
                                  blank=True,
                                  unique=True,
                                  verbose_name="Наименование модели")
    display_name = models.CharField(max_length=100,
                                    verbose_name="Наименование товара")
    code_model = models.CharField(max_length=10,
                                  unique=True,
                                  verbose_name="Код товара")
    article_number = models.CharField(max_length=15,
                                      unique=True,
                                      verbose_name="Артикул")
    description = models.CharField(max_length=200,
                                   verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="Цена товара")
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='product/images/',
        verbose_name='Изображения товара'
    )
    subcategory = models.ForeignKey(
        category.SubCategory,
        related_name='in_subcategory',
        on_delete=models.CASCADE,
        verbose_name="Категория товара"
    )
    attributes = models.ManyToManyField(
        Attribute,
        through=ProductAttribute,
        related_name="in_attribute"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        app_label = 'products'
        db_table = "products"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def get_tech_details(self):
        """
        Выводит основные характеристики
        """
        tech_detail_info = {
            "Производитель": self.manufacturer,
            "Модель": self.model_name
        }
        return {**tech_detail_info}

    def get_extra_info(self):
        """
        Возвращает дополнительную информацию о товаре
        """
        pass

    def get_title_prodcut(self):
        """
        Возвращает заглавие товара
        """
        title_data = (f'{self.subcategory.name} {self.manufacturer}'
                      f'{self.model_name}')

        return title_data

    def __str__(self):
        return (f"{self.model_name}: "
                f"{self.manufacturer} {self.code_model} - {self.price}")
