from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import StandardModel
from .validators import TelephoneNumberValidator


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер Юзера."""

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None,
                         **extra_fields):
        """Создание суперпользователя."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('type', CustomUser.Types.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_superuser(username, email, password,
                                      **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        """Создание и сохранения пользователя."""
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_superuser(self, username, email, password, **extra_fields):
        """Создание и сохранения суперпользователя."""
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = Admin(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, StandardModel):
    """Пользователь."""

    class Types(models.TextChoices):
        """Типы пользователей."""

        ADVERTISER = 'ADVERTISER', 'Advertiser'
        MODERATOR = 'MODERATOR', 'Moderator'
        ADMIN = 'ADMIN', 'Admin'

    base_type = Types.ADVERTISER
    objects = CustomUserManager()

    type = models.CharField(
        max_length=50,
        choices=Types.choices,
        default=Types.ADVERTISER,
        verbose_name='Тип пользователя',
    )
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

    @property
    def is_advertiser(self):
        return self.type == self.Types.ADVERTISER

    @property
    def is_moderator(self):
        return self.type == self.Types.MODERATOR

    @property
    def is_admin(self):
        return self.type == self.Types.ADMIN

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class AdvertiserManager(models.Manager):
    """Менеджер для Пользователей."""

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Types.ADVERTISER)


class ModeratorManager(models.Manager):
    """Менеджер для Модераторов."""

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Types.MODERATOR)


class AdminManager(models.Manager):
    """Менеджер для Админов."""

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Types.ADMIN)


class Advertiser(CustomUser):
    """Пользователь, который выкладывает объявление."""

    base_type = CustomUser.Types.ADVERTISER

    objects = AdvertiserManager()

    class Meta:
        proxy = True


class Moderator(CustomUser):
    """Модератор."""

    base_type = CustomUser.Types.MODERATOR

    objects = ModeratorManager()

    class Meta:
        proxy = True


class Admin(CustomUser):
    """Админ."""

    base_type = CustomUser.Types.ADMIN

    objects = AdminManager()

    class Meta:
        proxy = True
