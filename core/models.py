from django.db import models


class StandardModel(models.Model):
    """Стандартная модель."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        abstract = True


class MoneyField(models.DecimalField):
    """Тип для денег."""

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 16
        kwargs['decimal_places'] = 2
        super().__init__(*args, **kwargs)
