from datetime import datetime
from rest_framework.validators import ValidationError


def year_validator(value):
    """The validator checks the correctness of the entered date"""
    if value < 1900 or value > datetime.now().year:
        raise ValidationError(
            f'{value} is is not a correct year!'
        )
    return value
