from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

char_validator = UnicodeUsernameValidator()


def validate_username(value):
    """Запрет на использование 'me' в username"""
    if value == 'me':
        raise ValidationError(
            'Такое имя использовать запрещено'
        )
    return value
