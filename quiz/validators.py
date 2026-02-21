from django.core.exceptions import ValidationError

from quiz.constants import MIN_OPTIONS_COUNT


def validate_min_options(value):
    if not isinstance(value, list):
        raise ValidationError('Варианты ответа должны быть в виде списка.')

    if len(value) < MIN_OPTIONS_COUNT:
        raise ValidationError(
            'Количество вариантов ответа должно '
            + f'быть не меньше {MIN_OPTIONS_COUNT}.'
        )
