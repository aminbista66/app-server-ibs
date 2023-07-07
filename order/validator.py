from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_minimum(value):
    if value <= 0:
        raise ValidationError(
            _("%(value)s cannot be less than or equal to zero"),
            params={"value": value},
        )