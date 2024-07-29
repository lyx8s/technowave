from django.db import models
from django.conf import settings

from products.models.product import Product


class Configuration(models.Model):
    """
    Модель конфигурации
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "configuration"
        verbose_name = 'Конфигуратор'
        verbose_name_plural = 'Конфигураторы'

    def get_user_configuration(self):
        """
        Возвращает список компонентов, связанных с конфигурацией пользователя.
        """
        components_list = self.configuration_components.all().select_related('component')
        configuration_details = [
            {
                'component_id': component.component.id,
                'component_name': component.component.name,
                'component_price': component.component.price,
                'component_created_at': component.created_at,
                'component_updated_at': component.updated_at
            }
            for component in components_list
        ]
        return configuration_details

    def __str__(self):
        return f"{self.user}"


class Component(models.Model):
    """
    Модель компонентов, добавленных в конфигуратор
    """
    configuration = models.ForeignKey(
        Configuration,
        on_delete=models.CASCADE,
        related_name='configuration_components')
    component = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.CASCADE)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        db_table = "component"
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'

    def __str__(self):
        return f"{self.configuration}, {self.component}"
