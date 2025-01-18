from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r"^\+998([0-9]{9})$"            
    message = _(
        "Enter a valid phone. This value may contain only digits and /+/ character."
    )
    flags = 0
