import re

from django.core.exceptions import ValidationError


def validate_slug(value):
    """Проверка, чтоб 'slug' соответствовал по содержанию """

    if not re.match(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'Выбранные символы не подходят для slug'
        )
