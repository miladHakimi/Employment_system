from django.core.validators import RegexValidator

number = RegexValidator(r'^[09][0-9]*$', 'Only digits are allowed.')
