from django import template
register = template.Library()

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Возвращает параметр verbose_name из модели
    """
    return instance._meta.get_field(field_name).verbose_name.title()