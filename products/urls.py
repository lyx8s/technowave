from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

# ----- URL для обращения к категориям и подкатегориям -----

router.register(r'categories', views.CategoryViewSet,
                basename='categories')
router.register(r'categories/(?P<category_id>\d+)/subcategories',
                viewset=views.CategorySubCategoryViewSet,
                basename='category_subcategories_link')

# ----- URL для обращения к продуктам -----

router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'attributes', views.AttributeViewSet, basename='attributes')
router.register(r'categories/(?P<category_id>\d+)/subcategories/'
                r'(?P<subcategory_id>\d+)/products',
                views.ProductBySubCategoryViewSet,
                basename='products_by_subcategories_link')

urlpatterns = [
    path('', include(router.urls)),
]
