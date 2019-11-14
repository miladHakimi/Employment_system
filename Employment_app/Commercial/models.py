import datetime

from django.db import models

from Accounting.models import Employer


class Ad(models.Model):
    employer = models.ForeignKey(
        Employer,
        related_name='ads',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=50
    )
    img = models.ImageField(
        name="profile_img",
        blank=True
    )
    expDate = models.DateField(
        default=datetime.date.today,
        blank=True
    )
    FIELD_CHOICES = [('programming', 'Programmer'), ('mechanical_engineering', 'Mechanical Engineer')]
    fieldsOfExpertise = models.CharField(
        choices=FIELD_CHOICES,
        max_length=20
    )
    salary = models.CharField(
        max_length=10
    )