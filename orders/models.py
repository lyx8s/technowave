import uuid
from django.db import models
from django.db import transaction

from users.models import CustomUser
from products.models.product import Product


ORDER_STATUS = {
    "PROCCESING": 'В обработке',
    "SENT": 'Отправлен',
    "DELIVERED": 'Доставлен'
}


class ShoppingCart(models.Model):
    """
    Корзина
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец корзины")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_price(self):
        self.total_price = sum(item.get_cost() for item in self.cart_items.all())
        self.save()

    def __str__(self):
        return f'Корзина {self.user} - {self.total_price}'

    class Meta:
        db_table = "shoppingCart"
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """
    Элементы корзины
    """
    cart = models.ForeignKey(ShoppingCart,
                             on_delete=models.CASCADE,
                             related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        verbose_name="Кол-во товара",
        default=1
    )

    def get_cost(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.quantity} x {self.product}'
    
    class Meta:
        db_table = "cartItems"
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'



class Order(models.Model):
    """
    Модель заказа
    """
    order_id = models.UUIDField(primary_key=True, 
                                default=uuid.uuid4,
                                editable=False,
                                verbose_name="Номер заказа")
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Заказчик")
    status = models.CharField(
        choices=ORDER_STATUS,
        default=ORDER_STATUS['PROCCESING'])
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0,
        verbose_name="Общая стоимость")
    shipping_address = models.TextField(
            verbose_name="Адрес доставки")
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        verbose_name='Список товара')

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление заказа")

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.cart.cart_items.all())

    def update_total_price(self):
        self.total_price = self.get_total_cost()
        self.save()

    def __str__(self):
        return f'Заказ {self.order_id}'

    class Meta:
        db_table = "orders"
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)
