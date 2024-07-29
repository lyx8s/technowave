from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from . import models


class CustomUserSerializer(UserSerializer):
    """
    Пользовательский сериализатор
    """

    class Meta:
        model = models.CustomUser
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'phone_number'
                  )


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор создания пользователя
    """

    password = serializers.CharField(style={"input_type": "password"},
                                     write_only=True)

    class Meta:
        model = models.CustomUser
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'password'
                  )

    def validate_username(self, value):
        """
        Валидация имени пользователя
        """
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me'" 'в качестве `username`' ' запрещено.'
            )
        return value
