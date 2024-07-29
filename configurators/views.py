from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404

from api.common import services_db
from .models import Configuration, Component
from products.models.product import Product
from orders.models import CartItem
from .serializers import (ConfigurationSerializer, CreateConfigurationSerializer,
                         ComponentSerializer, CreateComponentSerializer,
                         ComponentBySearchSerializer)
from orders.permissions import IsCurrentUserOrAccessIsDenied
from products.serializers import ProductCartSerializer
from products.paginations import CustomPagination


class ConfigurationsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет конфигурций
    """

    serializer_class = ConfigurationSerializer
    permission_classes = (IsCurrentUserOrAccessIsDenied,)
    http_method_names = ('get', 'delete')
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Configuration.objects.filter(user=user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists() and not request.user.is_staff:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(ConfigurationsViewSet, self).list(request, *args, **kwargs)


class ComponentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет компонента
    """

    queryset = services_db.all_objects(Component.objects)
    serializer_class = ComponentSerializer
    http_method_names = ('get','post','delete',)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class
        return CreateComponentSerializer
    
    def list(self, request, *args, **kwargs):
        serializer = ComponentBySearchSerializer(data=request.data)
        if serializer.is_valid():
            search_value = serializer.validated_data.get('search')
            queryset = Product.objects.filter(subcategory__name__icontains=search_value)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ProductCartSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ProductCartSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=False, methods=('post', 'delete',))
    def add_component(self, request, component_id):
        """
        Добавить компонент в конфигурацию
        """
        configuration = self.get_object()
        component_id = request.data.get('component_id')
        quantity = request.data.get('quantity', 1)

        if not component_id and quantity:
            return Response(
                {'error': 'Выберите компонент!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            component = Product.objects.get(id=component_id)
            # Проверка на обязательные компоненты (пример условия)
            if not component.is_required:
                return Response({'error': 'Этот компонент не является обязательным.'}, status=400)

            # Проверка, существует ли уже компонент в конфигурации
            if Component.objects.filter(configuration=configuration, component=component).exists():
                return Response({'error': 'Компонент уже добавлен в конфигурацию.'}, status=400)

            # Создание нового компонента в конфигурации
            Component.objects.create(configuration=configuration, component=component)
            # Создание или обновление элемента корзины
            cart_item, created = CartItem.objects.get_or_create(
                configuration=configuration,
                component=component,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response({'success': 'Компонент добавлен в конфигурацию.'})

        except Product.DoesNotExist:
            return Response({'error': 'Компонент не найден.'}, status=404)

            
