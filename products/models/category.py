from pytils.translit import slugify
from django.db import models
from django.core.validators import FileExtensionValidator


STORE_CATEGORY = [
    "Комьютеры и ноутбуки",
    "Комплектующие для ПК",
    "Перефирия",
    "Серверы и СХД"
]


class Category(models.Model):
    """
    Подкатегории товаров
    """
    name = models.CharField(
        max_length=100,
    )
    slug = models.SlugField(
        max_length=75,
        unique=True,
        editable=False,
    )
    image = models.FileField(
        upload_to="pictures/categories/images",
        validators=[FileExtensionValidator(['svg'])],
        null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        app_label = 'products'
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)


class SubCategory(models.Model):
    """
    Модель подкатегорий товара
    """

    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        max_length=75,
        unique=True,
        editable=False
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='pictures/subcategories/images',
        verbose_name='Иконка подкатегории'
    )
    category = models.ForeignKey(Category,
                                 related_name='in_category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    class Meta:
        app_label = 'products'
        db_table = 'subcategories'
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
