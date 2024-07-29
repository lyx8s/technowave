def all_objects(object):
    """
    Возращает все объекты модели
    """
    return object.all()


def filter_objects(object, **kwargs):
    """
    Возращает отфильтрованные объекты модели.
    Принимает n кол-во именновых агрументов
    """
    return object.filter(**kwargs)


def create_object(object, **kwargs):
    """
    Создает объект модели
    """
    return object.create(**kwargs)


def get_object(object, **kwargs):
    """
    Возвращает один объект из модели
    """
    return object.get(**kwargs)


def delete_object(object):
    return object.delete()
