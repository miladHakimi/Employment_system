from django.core import validators
from django.utils.translation import gettext_lazy as _


class PhoneValidator(validators.RegexValidator):
    regex = r'^0\d{10}$'
    message = _(
        'Invalid phone number. It should be an 11 digit number starting with "0".'
    )
