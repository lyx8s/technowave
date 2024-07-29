from rest_framework import serializers

from .models import Configuration, Component
from products.models.product import Product
from products.serializers import ProductInAddedSerializer


class ComponentSerializer(serializers.ModelSerializer):
    """
    Сериализатора для компонентов
    """

    component = ProductInAddedSerializer()

    class Meta:
        model = Component
        fields = (
            'id',
            'configuration',
            'component'
        )

class CreateComponentSerializer(serializers.ModelSerializer):
    """
    Сериализатора для создания компонентов
    """

    class Meta:
        model = Component
        fields = (
            'id',
            'configuration',
            'component'
        )




class ConfigurationSerializer(serializers.ModelSerializer):
    """
    Сериализатора для конфигураций
    """

    components = ComponentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Configuration
        fields = (
            'id',
            'user',
            'components'
        )


class CreateConfigurationSerializer(serializers.ModelSerializer):
    """
    Сериализатора для создания конфигурации
    """

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Configuration
        fields = (
            'id',
            'user'
        )
    
    def create(self, validated_data):
        # Создание нового экземпляра модели
        instance = Configuration.objects.get_or_create(**validated_data)
        return instance


class ComponentBySearchSerializer(serializers.Serializer):
    """
    Сериализатор для найденных компонентов
    """

    search = serializers.CharField(max_length=100)

    def validate_search(self, value):
        """
        Проверяем, что строка поиска не пуста.
        """
        if not value.strip():
            raise serializers.ValidationError("Строка поиска не может быть пустой.")
        return value