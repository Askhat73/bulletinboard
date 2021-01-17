from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import ugettext_lazy as _


@deconstructible
class TelephoneNumberValidator(RegexValidator):
    """Проверяет номера телефонов."""
    regex = _lazy_re_compile(r'^((7|8)\d{10})$')
    message = _('Неверный формат телефонного номера.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __eq__(self, other):
        return (
                isinstance(other, TelephoneNumberValidator) and
                super().__eq__(other)
        )
