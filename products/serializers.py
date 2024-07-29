from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import category, product
from api.serializers import Base64ImageField


# --------- Сериализатор для категорий товара ------------

class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категорий товара
    """

    class Meta:
        model = category.Category
        fields = (
            'id',
            'name',
            'image',
            'slug'
        )


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для подкатегорий товара
    """

    class Meta:
        model = category.SubCategory
        fields = (
            'name',
            'image',
            'slug',
        )

    def validate_name(self, value):
        get_category = category.SubCategory.objects.filter(
            name=value
        )
        if get_category.exists():
            raise ValidationError({"error": "Нельзя добавить подкатегорию, "
                                   "которая уже есть!"})
        return value


class CategorySubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка категорий
    и принадлежащих ему подкатегорий
    """

    subcategories = serializers.ReadOnlyField(
        source='category.Category.in_category'
    )

    class Meta:
        model = category.Category
        fields = (
            'name',
            'image',
            'slug',
            'subcategories'
        )


# --------- Сериализаторы для товара -----------------


class ProductCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для карточки товара
    """

    class Meta:
        model = product.Product
        fields = (
            'id',
            'image',
            'display_name',
            'description',
            'price'
        )


class ProductInAddedSerializer(serializers.ModelSerializer):
    """
    Сериализатор для товара, который куда-то добавили
    """

    class Meta:
        model = product.Product
        fields = (
            'id',
            'display_name',
            'image',
            'price'
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавление товара
    """

    image = Base64ImageField(
        required=False
    )

    class Meta:
        model = product.Product
        fields = (
            'id',
            'manufacturer',
            'model_name',
            'display_name',
            'code_model',
            'article_number',
            'description',
            'price',
            'image',
            'subcategory',
        )


class AttributeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для атрибутов
    """

    class Meta:
        model = product.Attribute
        fields = (
            'id',
            'title',
            'name'
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для товара
    """
    subcategory = SubCategorySerializer(read_only=True)
    image = Base64ImageField()
    attributes = AttributeSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = product.Product
        fields = (
            'id',
            'manufacturer',
            'model_name',
            'display_name',
            'code_model',
            'article_number',
            'description',
            'price',
            'image',
            'subcategory',
            'attributes'
        )


class CreateAttributeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания атрибутов
    """

    class Meta:
        model = product.Attribute
        fields = (
            'id',
            'title',
            'name'
        )

    def validate_title(self, value):
        title = value
        if not title:
            raise ValidationError("Введите имя!")

        name_exists = product.Attribute.objects.filter(title=title).exists()

        if name_exists:
            raise ValidationError("Такое имя уже есть!")

        return value

    def validate_name(self, value):
        name = value
        if not name:
            raise ValidationError("Введите имя!")

        name_exists = product.Attribute.objects.filter(name=name).exists()

        if name_exists:
            raise ValidationError("Такое имя уже есть!")

        return value


class CreateProductAttribute(serializers.ModelSerializer):
    """
    Сериализатор для добавления аттрибута к продукту
    """
    class Meta:
        model = product.ProductAttribute
        fields = ('__all__')

    def validate_attribute(self, value):
        attr = value
        if not attr:
            raise ValidationError({"message": "Выберите аттрибут!"})

        name_exists = product.Attribute.objects.filter(title=attr).exists()

        if name_exists:
            raise ValidationError("Такое имя уже есть!")

        return value

    def validate_product(self, value):
        name = value
        if not name:
            raise ValidationError("Введите имя!")

        name_exists = product.Attribute.objects.filter(name=name).exists()

        if name_exists:
            raise ValidationError("Такое имя уже есть!")

        return value


class ProductBySubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для товара,
    относящегося к определенной категории
    """
    subcategory = SubCategorySerializer()
    image = Base64ImageField()
    attributes = AttributeSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = product.Product
        fields = (
            'id',
            'manufacturer',
            'model_name',
            'display_name',
            'code_model',
            'article_number',
            'description',
            'price',
            'image',
            'subcategory',
            'attributes'
            )
