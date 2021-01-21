from typing import Optional

import requests
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from core.exceptions import RecaptchaConnectionServerError


class RecaptchaCheckService:
    """Сервис проверки Recaptcha."""

    def __call__(self, response_token: str) -> Optional[bool]:
        """Проверяет Recaptcha."""

        recaptcha_response = self._get_recaptcha_json_response(response_token)
        if recaptcha_response.get('success'):
            return True
        return False

    def _get_recaptcha_json_response(self, response_token: str):
        """Получает JSON ответ Recaptcha"""
        response = self._get_recaptcha_response(response_token=response_token)
        try:
            response.raise_for_status()
        except requests.RequestException:
            raise RecaptchaConnectionServerError(
                _('Connection to reCaptcha server failed')
            )
        else:
            return response.json()

    def _get_recaptcha_response(self, response_token: str):
        """Получает ответ Recaptcha"""
        return requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': response_token,
            },
            timeout=5,
        )


