from django.contrib.admin import ModelAdmin, register

from .models import product, category


@register(product.Product)
class ProductAdmin(ModelAdmin):
    list_display = (
            'id',
            'manufacturer',
            'model_name',
            'display_name',
            'code_model',
            'article_number',
            'description',
            'price',
            'image',
            'get_attributes',
            'subcategory',
        )

    def get_attributes(self, obj):
        if obj.attributes.all():
            return list(obj.attributes.all().values_list('in_attribute', flat=True))
        else:
            return 'NA'


@register(product.Attribute)
class AttributeAdmin(ModelAdmin):
    list_display = (
        'id',
        'title',
        'name'
    )


@register(product.ProductAttribute)
class ProductAttributeAdmin(ModelAdmin):
    list_display = (
        'product',
        'attribute',
        'value'
    )


@register(category.Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        'name',
        'image'
    )
