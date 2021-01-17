from django.contrib.auth import get_user_model


class CheckPhoneExistsService:
    """Сервис проверки налачия телефона в БД."""

    def __call__(self, phone_number: str) -> bool:
        """Проверяет наличие телефона в БД."""

        User = get_user_model()
        return User.objects.filter(phone=phone_number).exists()


class FormatPhoneNumberService:
    """Сервис приведения номера телефона в формат 7XXXXXXXXXX."""

    def __call__(self, phone_number: str) -> str:
        """Приводит номер телефона в формат 7XXXXXXXXXX."""

        if len(phone_number) == 10:
            phone_number = f'7{phone_number}'
        elif len(phone_number) == 11 and phone_number[0] == '8':
            phone_number = f'7{phone_number[1:]}'

        return phone_number
