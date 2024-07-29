from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from . paginations import CustomPagination
from .models import category, product
from . import serializers
from orders.models import ShoppingCart, CartItem
from . import mixins
from api.common import services_db
from .permissions import IsAdminOrReadOnly
from .services.add_to import AddTo
from .services.delete_to import DeleteTo
from .filters import ProductFilter


# --------- Вьюсеты для категорий товара ------------


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Вьюсет категорий
    """
    queryset = category.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True,
            methods=['post'])
    def add_subcategory(self, request, pk=None):
        """
        Добавляет подкатегорию к категории по слагу
        """
        category = self.get_object()
        serializer = serializers.SubCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategorySubCategoryViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для категори и их подкатегорий
    """

    queryset = category.SubCategory.objects.all()
    serializer_class = serializers.CategorySubCategorySerializer
    http_method_names = ('get','delete',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')

        subcategory_queryset = services_db.filter_objects(
            self.queryset,
            category__id = category_id
        )
        if category_id:
            return subcategory_queryset
        return self.queryset

    def destroy(self, request, *args, **kwargs):
        try:
            category_id = self.kwargs.get('category_id')
            subcategory_id = kwargs.get('pk')
            subcategory_obj = get_object_or_404(category.SubCategory, category__id=category_id, pk=subcategory_id)
            services_db.delete_object(
                subcategory_obj
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except category.SubCategory.DoesNotExist:
            return Response({'message': 'Подкатегория не найдена.'}, status=status.HTTP_404_NOT_FOUND)


# --------- Вьюсеты для товара -----------------

class ProductViewSet(viewsets.ModelViewSet):
    """
    Вьюсет товара
    """
    queryset = services_db.all_objects(product.Product.objects)
    serializer_class = serializers.ProductSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ('subcategory__name', )
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class
        return serializers.ProductCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        product_pk = kwargs.get('pk')
        product_data = get_object_or_404(product.Product, id=product_pk)

        response = super(ProductViewSet, self).update(request, *args, **kwargs)

        if response.status_code == 200:
            cart_items = CartItem.objects.filter(product=product_data)
            for item in cart_items:
                item.price = product_data.price
                item.save()

            shopping_cart = get_object_or_404(ShoppingCart, user=user)
            shopping_cart.update_total_price()

        return response


    @action(detail=True,
            methods=('POST', 'DELETE'),
            permission_classes=(IsAuthenticated,))
    def cart(self, request, pk):
        """
        Добавить товар в корзину
        """
        user = request.user
        if request.method == 'POST':
            value = AddTo().add_to(product_pk=pk, model=CartItem, user=user)
            if value is True:
                return Response({'errors': ('Вы уже добавили этот товар!')},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = serializers.ProductInAddedSerializer(
                value.product
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            value = DeleteTo().delete_to(product_pk=pk, model=CartItem, user=user)
            if value:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Ошибка удаления, такого товара нет'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=True,
            methods=('POST', 'PATCH'))
    def add_attribute(self, request, pk):
        """
        Добавить атрибут к товару
        """
        product_data = get_object_or_404(product.Product, id=pk)
        if request.method == 'POST':
            serializer = serializers.CreateAttributeSerializer(
                data=request.data
            )
            if serializer.is_valid():
                serializer.save()

            attr_data = serializer.validated_data

            attribute = get_object_or_404(
                product.Attribute,
                **attr_data
            )

            product.ProductAttribute.objects.create(
                product=product_data,
                attribute=attribute
            )

            return Response(
                {"success": "Атрибут успешно добавлен к товару."},
                status=status.HTTP_201_CREATED
            )



class AttributeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет атрибутов
    """

    queryset = product.Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class
        return serializers.CreateAttributeSerializer


class ProductBySubCategoryViewSet(viewsets.ModelViewSet):
    """
    Вьсет для продуктов, относящихся
    к определенным подкатегориям
    """

    serializer_class = serializers.ProductBySubCategorySerializer
    http_method_names = ('get',)
    pagination_class = CustomPagination

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        subcategory_id = self.kwargs.get("subcategory_id")

        subcategory_obj = get_object_or_404(
            category.SubCategory,
            id=subcategory_id
        )
        category_obj = get_object_or_404(
            category.Category,
            id=category_id
        )

        product_queryset = product.Product.objects.filter(
            subcategory=subcategory_obj,
            subcategory__category=category_obj
        )
        return product_queryset
