from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCount

from users.models import StandardModel


class Category(StandardModel):
    """Категория объявления."""

    name = models.CharField(max_length=200, verbose_name='Название категории')
    slug = models.SlugField(max_length=40, unique=True, verbose_name='Код')
    description = models.TextField(verbose_name='Описание')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='Родительская категория',
    )
    sort = models.IntegerField(verbose_name='Порядок сортировки')

    def __str__(self):
        return self.name


class MoneyField(models.DecimalField):
    """Тип для денег."""

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 16
        kwargs['decimal_places'] = 2
        super().__init__(*args, **kwargs)


class Region(StandardModel):
    """Регион."""

    name = models.CharField(max_length=50, verbose_name='Название региона')

    def __str__(self):
        return self.name


class City(StandardModel):
    """Город."""

    name = models.CharField(max_length=50, verbose_name='Название города')
    region = models.ForeignKey(
        'Region',
        on_delete=models.CASCADE,
        default=0,
        verbose_name='Название региона',
    )
    slug = models.SlugField(max_length=50, verbose_name='Код')

    def __str__(self):
        return self.name


class Ad(StandardModel):
    """Объявление."""

    class AdStatus(models.IntegerChoices):
        """Статус объявления."""

        DRAFT = 1, _('Черновик')
        MODERATION = 2, _('На модерации')
        CANCELED = 3, _('Отклонено')
        REMOVED = 4, _('Снято / продано')
        ACTIVE = 5, _('Активно')

    name = models.CharField(max_length=200, verbose_name='Название объявления')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='ads',
        null=True,
        verbose_name='Категория объявления',
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        related_name='ads',
        null=True,
        verbose_name='Город'
    )
    description = models.TextField(verbose_name='Описание')
    publication_date = models.DateTimeField(verbose_name='Дата публикации')
    price = MoneyField(verbose_name='Стоимость')
    seller = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Продавец',
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation',
        verbose_name='Просмотры',
    )
    status = models.PositiveSmallIntegerField(
        choices=AdStatus.choices,
        verbose_name='Статус объявления',
    )

    def __str__(self):
        return self.name


class Photo(StandardModel):
    """Фотография в объявлении."""

    ad = models.ForeignKey(
        'Ad',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Объявление',
    )
    image = models.ImageField(
        upload_to=settings.PHOTO_UPLOAD_DIR,
        verbose_name='Изображение',
    )

    def __str__(self):
        return str(self.ad)


class ModerationEntry(StandardModel):
    """Запись о модерации объявления."""

    class Decision(models.IntegerChoices):
        """Решение модератора."""

        PUBLISH = 1, _('Опубликовать')
        REVISION = 2, _('Отправить на доработку')

    ad = models.ForeignKey(
        'Ad',
        models.CASCADE,
        related_name='moderation_entry',
        verbose_name='Объявление',
    )
    moderator = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='moderation_entries',
        verbose_name='Модератор',
    )
    decision = models.PositiveSmallIntegerField(
        choices=Decision.choices,
        verbose_name='Статус объявления',
    )
    reason = models.CharField(
        max_length=200,
        verbose_name='Причина отклонения к доработке',
    )

    def __str__(self):
        return str(self.ad)
