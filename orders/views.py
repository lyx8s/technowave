from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Order, ShoppingCart, CartItem
from api.common import services_db
from .serializers import OrderSerializer, CreateOrderSerializer, CartShortInfoSerializer
from .permissions import IsCurrentUserOrAccessIsDenied
from products.paginations import CustomPagination


class OrderViewSet(viewsets.ModelViewSet):
    """
    Вьюсет заказов
    """

    queryset = services_db.all_objects(Order.objects)
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post')
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class
        return CreateOrderSerializer
    
    def get_queryset(self):
        user=self.request.user
        order = services_db.filter_objects(
            Order.objects,
            user=user
        )
        return order
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        shoppingCart = get_object_or_404(
            ShoppingCart,
            user=user
        )
        order = services_db.create_object(
            Order.objects,
            user=user,
            cart=shoppingCart
        )
        order.update_total_price()
        CartItem.objects.filter(cart=shoppingCart).delete()
        services_db.delete_object(
            shoppingCart
        )
        serializer = CreateOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    Вьсет для корзины товаров
    """

    serializer_class = CartShortInfoSerializer
    permission_classes = (IsCurrentUserOrAccessIsDenied,)
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        cart = services_db.filter_objects(
            ShoppingCart.objects,
            user=user
        )
        return cart