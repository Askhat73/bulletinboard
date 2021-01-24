from allauth.account.utils import get_next_redirect_url
from allauth.account.views import LoginView
from django.conf import settings
from django.views.generic import TemplateView

from users.mixins import UserTypeIsAdvertiserMixin, UserTypeIsModeratorMixin, \
    UserTypeIsAdminMixin


class CustomLoginView(LoginView):

    def get_context_data(self, *args, **kwargs):
        context = super(CustomLoginView, self).get_context_data(*args, **kwargs)
        context['recaptcha_public_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def get_success_url(self):
        """Получает ссылку для редиректа после успешной авторизации."""
        return get_next_redirect_url(self.request, self.redirect_field_name)



class AdvertiserLkView(UserTypeIsAdvertiserMixin, TemplateView):
    """Личный кабинет Пользователя."""

    template_name = 'lk/advertiser.html'


class ModeratorLkView(UserTypeIsModeratorMixin, TemplateView):
    """Личный кабинет Модератора."""

    template_name = 'lk/moderator.html'


class AdminLkView(UserTypeIsAdminMixin, TemplateView):
    """Личный кабинет Админа"""

    template_name = 'lk/admin.html'
