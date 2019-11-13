from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from Accounting.validators import PhoneValidator


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )
    groups = ""
    user_permissions = [AllowAny]
    username = models.CharField(
        _('user name'),
        unique=True,
        max_length=50,
    )
    USERNAME_FIELD = 'username'


class Applicant(User):
    firstName = models.CharField(
        _('first name'),
        max_length=50
    )
    lastName = models.CharField(
        _('last name'),
        max_length=50
    )
    age = models.IntegerField(
        _('Age'),
        default=18,
        blank=True,
    )
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=20
    )
    # todo: verify phone
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )
    objects = UserManager()

    def __str__(self):
        return self.firstName + " " + self.lastName


class Employer(User):
    companyName = models.CharField(
        _('company name'),
        max_length=50
    )
    establishedYear = models.DateTimeField(
        _('established year'),
        default=timezone.now,
    )
    address = models.CharField(
        _('Address'),
        max_length=200,
        blank=True,
    )

    # todo: verify phone
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        validators=[PhoneValidator()]
    )
    objects = UserManager()

    def __str__(self):
        return self.companyName

