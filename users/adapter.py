import time
from typing import Optional

from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.services import RecaptchaCheckService
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

    def authenticate(self, request, **credentials):
        user = super(CustomAccountAdapter, self).authenticate(
            request,
            **credentials,
        )
        if self._is_attempts_limit_reached(request, **credentials):
            self._set_session_captcha_is_required(request)
        return user



    def pre_authenticate(self, request, **credentials):
        """Выполняется перед аутенфикацией пользователя."""

        if self._is_attempts_limit_reached(request, **credentials):
            self._set_session_captcha_is_required(request)
            captcha = request.POST.get('g-recaptcha-response')
            if not RecaptchaCheckService()(captcha):
                raise forms.ValidationError(
                    _('Необходимо пройти проверку от роботов.'),
                )

    def _set_session_captcha_is_required(self, request):
        """Устанавливает в сессию значение о необходимости ввода каптчи."""
        request.session['captcha_is_required'] = True

    def _get_current_attempt_time(self):
        """Получает время текущей попытки."""

        dt = timezone.now()
        return time.mktime(dt.timetuple())

    def _is_attempts_limit_reached(self, request, **credentials) -> bool:
        """Условие для вывода каптчи."""

        login_data = self._get_login_data(request, **credentials)
        if login_data:
            dt = timezone.now()
            current_attempt_time = time.mktime(dt.timetuple())
            expire_time = login_data[-1] + settings.ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT
            time_is_not_expired = current_attempt_time < expire_time
            login_attempts_limit_is_reached = len(login_data) >= settings.ACCOUNT_LOGIN_ATTEMPTS_LIMIT
            return login_attempts_limit_is_reached and time_is_not_expired
        return False

    def _get_login_data(self, request, **credentials):
        """Получает данные попыток авторизации по логину."""

        cache_key = self._get_login_attempts_cache_key(
            request,
            **credentials
        )
        return cache.get(cache_key, None)
