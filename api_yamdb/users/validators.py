import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            ('Не допустимые символы в нике.'),
        )
