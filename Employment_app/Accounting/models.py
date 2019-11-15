import datetime
from datetime import timedelta

import jwt
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from Accounting.validators import PhoneValidator
from Employment_app import settings


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


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
    # user_type = ""
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


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
    objects = MyUserManager()

    def __str__(self):
        return self.firstName + " " + self.lastName


class Employer(User):
    user_type = 'emp'
    objects = MyUserManager()

    companyName = models.CharField(
        _('company name'),
        max_length=50
    )
    establishedYear = models.DateTimeField(
        _('established year'),
        default=datetime.datetime.today(),
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
