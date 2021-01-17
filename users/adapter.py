from typing import Optional

from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.utils.translation import gettext_lazy as _

from .services import CheckPhoneExistsService


class CustomAccountAdapter(DefaultAccountAdapter):

    def validate_unique_phone(self, phone: str) -> Optional[str]:
        """Валидирует телефон на уникальность."""

        if CheckPhoneExistsService()(phone):
            raise forms.ValidationError(
                _('Пользователь с таким телефоном уже зарегистрирован.'),
            )
        return phone

    def save_user(self, request, user, form, commit=True):
        """Сохраняет нового пользователя."""

        from allauth.account.utils import user_field

        data = form.cleaned_data
        user.phone = data.get('phone')
        middle_name = data.get('middle_name')
        if middle_name:
            user_field(user, 'middle_name', middle_name)
        user = super(CustomAccountAdapter, self).save_user(request, user, form,
                                                           commit)
        return user
