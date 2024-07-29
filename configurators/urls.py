from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'configurations', views.ConfigurationsViewSet,
                basename='confugurations')
router.register(r'components', views.ComponentViewSet,
                basename='components')

urlpatterns = [
    path('', include(router.urls)),
]
