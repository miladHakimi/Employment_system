from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models


class Applicant(AbstractBaseUser):
    firstName = models.CharField(
        _('first name'),
        max_length=50
    )
    lastName = models.CharField(
        _('last name'),
        max_length=50
    )
    userName = models.CharField(
        _('user name'),
        max_length=50
    )
    Age = models.IntegerField(
        _('Age'),
        default=18,
        blank=True,
    )
    GENDER_CHOICES = [('male', 'male'), ('female', 'female')]
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

    def __str__(self):
        return self.firstName + " " + self.lastName


class Employer(AbstractBaseUser):
    companyName = models.CharField(
        _('company name'),
        max_length=50
    )
    establishedYear = models.DateTimeField(
        _('established year'),
        default=timezone.now,
    )
    userName = models.CharField(
        _('user name'),
        max_length=50
    )
    Address = models.CharField(
        _('Address'),
        max_length=200,
        blank=True,
    )

    # todo: verify phone
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.companyName

