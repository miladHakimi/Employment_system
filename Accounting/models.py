from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from rest_framework.authtoken.models import Token

from Accounting.managers import MyUserManager
from Accounting.validators import PhoneValidator


class User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="chatuser_set",
        related_query_name="user",
    )
    username = models.CharField(
        _('user name'),
        unique=True,
        max_length=50,
    )
    USERNAME_FIELD = 'username'

    USER_CHOICES = [
        ('emp', 'Employer'),
        ('app', 'Applicant')
    ]
    user_type = models.CharField(
        choices=USER_CHOICES,
        blank=True,
        null=True,
        max_length=20
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )

    FIELD_CHOICES = [
        ('prog', 'Programmer'),
        ('mech', 'Mechanical Engineer')
    ]
    fieldsOfExpertise = MultiSelectField(
        choices=FIELD_CHOICES,
        max_length=20,
        blank=True,
        max_choices=3
    )

    def is_employer(self):
        return self.user_type == 'emp'

    def is_applicant(self):
        return self.user_type == 'app'


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
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=20
    )
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        validators=[PhoneValidator()]

    )
    cv = models.FileField(
        blank=True,
        null=True
    )
    objects = MyUserManager()

    def __str__(self):
        return self.firstName + " " + self.lastName


class Employer(User):
    objects = MyUserManager()

    companyName = models.CharField(
        _('company name'),
        max_length=50,
        blank=True,
        null=True
    )
    establishedYear = models.DateTimeField(
        _('established year'),
        default=datetime.today(),
        blank=True,
        null=True
    )
    address = models.CharField(
        _('Address'),
        max_length=200,
        blank=True,
    )
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        validators=[PhoneValidator()]
    )

    def __str__(self):
        return self.companyName
