from django.shortcuts import get_object_or_404

from api.common import services_db
from products.models import product
from orders.models import CartItem, ShoppingCart


class DeleteTo:

    def _get_product(self, product_pk):
        """
        Возвращает товар
        """
        product_data = get_object_or_404(
            product.Product,
            pk=product_pk
        )
        return product_data

    def _get_model(self, product_data, shopping_cart, model):
        """
        Возвращает объект, переданной модели
        или 404
        """
        obj = get_object_or_404(
            model,
            product=product_data,
            cart=shopping_cart
        )
        return obj

    def _check_product_exists(pk, product_data, model):
        """
        Проверяет, существует ли товар в модели
        """
        curr_model = services_db.filter_objects(
                model.objects,
                product=product_data
            ).exists()
        return curr_model

    def _delete_product(self, obj):
        """
        Удаляет товар
        """
        return services_db.delete_object(obj)

    def delete_to(self, user, product_pk, model):
        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=user
        )
        product_data = self._get_product(product_pk)
        obj = self._get_model(product_data, shopping_cart, model)
        is_added = self._check_product_exists(product_data, model)
        if is_added:
            deleted = self._delete_product(obj)
            shopping_cart.update_total_price()
            return deleted
        return is_added
