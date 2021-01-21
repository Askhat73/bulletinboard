from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from users.services import FormatPhoneNumberService
from users.validators import TelephoneNumberValidator


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'username', 'phone')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'username', 'phone')


class CustomSignupForm(SignupForm):
    """Форма регистрации пользователя."""

    phone = forms.CharField(
        label=_("Телефон"),
        validators=[TelephoneNumberValidator()],
        widget=forms.TextInput(
            attrs={"placeholder": _("Телефон"), "autocomplete": "Телефон"}
        ),
    )
    first_name = forms.CharField(
        label=_("Имя"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Имя"), "autocomplete": "Имя"}
        ),
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Фамилия"), "autocomplete": "Фамилия"}
        ),
    )
    middle_name = forms.CharField(
        label=_("Отчество"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Отчество"), "autocomplete": "Отчество"}
        ),
        required=False,
    )
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    def clean_phone(self):
        value = self.cleaned_data["phone"]
        value = FormatPhoneNumberService()(value)
        value = self.validate_unique_phone(value)
        return value

    def validate_unique_phone(self, value):
        return get_adapter().validate_unique_phone(value)


class CustomLoginForm(LoginForm):
    """Форма авторизации пользователя."""

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
