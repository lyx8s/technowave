from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser

from . import serializers
from . import models


class CustomUserViewSet(UserViewSet):
    """
    Пользовательский вьюсет
    """

    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser,)
