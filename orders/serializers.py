from rest_framework import serializers

from .models import Order, ShoppingCart
from products.serializers import ProductInAddedSerializer


class CartShortInfoSerializer(serializers.ModelSerializer):

    cart_items = ProductInAddedSerializer()
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения заказа
    """

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'total_price',
            'shipping_address',
            'cart',
            'created_at',
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения заказа
    """

    shipping_address = serializers.CharField(
        max_length=100,
        required=True
    )

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'total_price',
            'shipping_address',
            'cart',
            'created_at',
        )