from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.apps import apps

from .managers import UserManager


class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')]),
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Номер телефона',
        validators=([RegexValidator(
            regex=r'^\+7\d+$',
            message="Введите номер телефона формата: +79999999999 ")]
            )
    )

    # objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',
                       'first_name',
                       'last_name',
                       'phone_number',
                       'password'
                       )
    
    def get_configuration(self):
        """
        Возвращает последнюю конфигурацию, созданную пользователем.
        """
        
        Configuration = apps.get_model('configurators', 'Configuration')
        return Configuration.objects.filter(user=self).order_by('-created_at').first()

    def __str__(self):
        return f'{self.username}, {self.email}'
