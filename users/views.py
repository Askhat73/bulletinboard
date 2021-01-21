from allauth.account.views import LoginView
from django.conf import settings


class CustomLoginView(LoginView):

    def get_context_data(self, *args, **kwargs):
        context = super(CustomLoginView, self).get_context_data(*args, **kwargs)
        context['recaptcha_public_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context
