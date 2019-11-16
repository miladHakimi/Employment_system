import datetime

from django.db import models

from Accounting.models import Employer, Applicant
from Accounting.validators import IsNumberValidator


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
    FIELD_CHOICES = [
        ('prog', 'Programmer'),
        ('mech', 'Mechanical Engineer')
    ]
    fieldsOfExpertise = models.CharField(
        choices=FIELD_CHOICES,
        max_length=20
    )
    salary = models.CharField(
        max_length=10,
        validators=[IsNumberValidator]
    )
    picture = models.ImageField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title + "   " + self.employer.companyName


class Request(models.Model):
    applicant = models.ForeignKey(
        Applicant,
        related_name='request',
        on_delete=models.SET_NULL,
        null=True
    )
    ad = models.ForeignKey(
        Ad,
        related_name='ad',
        on_delete=models.SET_NULL,
        null=True,
    )
    accepted = models.BooleanField(
        null=True,
        default=False,
    )
    rejected = models.BooleanField(
        null=True,
        default=False,
    )

    def get_cv(self):
        return self.applicant.get_cv()

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.ad.title + "    " + self.applicant.username


class Appointment(models.Model):
    employer = models.ForeignKey(
        Employer,
        related_name='employer',
        on_delete=models.SET_NULL,
        null=True
    )
    applicant = models.ForeignKey(
        Applicant,
        related_name='aplicant',
        on_delete=models.SET_NULL,
        null=True
    )
    date = models.DateTimeField(
        null=True,
    )
