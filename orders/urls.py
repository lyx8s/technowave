from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'order', views.OrderViewSet,
                basename='orders')
router.register(r'show-cart', views.ShoppingCartViewSet,
                basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
