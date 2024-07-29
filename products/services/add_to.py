import functools
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from api.common import services_db
from products.models import product
from orders.models import CartItem, ShoppingCart


class AddTo:

    def _get_product(self, product_pk):
        """
        Вернуть товар, который нужно добавить
        """
        product_data = get_object_or_404(
            product.Product,
            pk=product_pk
        )
        return product_data

    def _check_model_exists(pk, product_data, model, shopping_cart):
        """
        Возвращает true, если существует запись у
        пользователя
        """
        is_added = services_db.filter_objects(
                model.objects,
                product=product_data,
                cart=shopping_cart
            ).exists()
        return is_added


    def _create_model(self, product_data, model, shopping_cart):
        """
        Создать запись в модели
        """
        obj = services_db.create_object(
            model.objects,
            product=product_data,
            cart=shopping_cart
        )
        return obj

    def add_to(self, product_pk, model, user):
        """
        Добавить товар к определенной модели.
        Пользователь не обязательный агрумент
        """
        shopping_cart, created = ShoppingCart.objects.get_or_create(
            user=user
        )
        product_data = self._get_product(product_pk)
        is_added = self._check_model_exists(product_data, model, shopping_cart)
        if is_added:
            return is_added
        obj = self._create_model(product_data, model, shopping_cart)
        shopping_cart.update_total_price()
        return obj
