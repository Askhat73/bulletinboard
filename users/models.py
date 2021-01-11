from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import StandardModel
from .validators import TelephoneNumberValidator


class CustomUser(AbstractUser, StandardModel):
    """Пользователь."""

    email = models.EmailField(unique=True, verbose_name='Email')
    middle_name = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='Отчество',
    )
    phone = models.CharField(
        unique=True,
        max_length=13,
        validators=[TelephoneNumberValidator()],
        verbose_name='Номер телефона',
    )
    convenient_time = models.TextField(verbose_name='Удобное время')
    REQUIRED_FIELDS = ['email', 'phone']
