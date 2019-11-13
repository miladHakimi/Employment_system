from django.db import models
from django.utils import timezone


class Ad(models.Model):
    title = models.CharField(
        max_length=50
    )
    img = models.ImageField(
        name="profile_img"
    )
    exp_data = models.DateField(
        default=timezone.now,
    )
    FIELD_CHOICES = [('programming', 'Programmer'), ('mechanical_engineering', 'Mechanical Engineer')]
    fieldsOfExpertise = models.CharField(
        choices=FIELD_CHOICES
    )
    salary = models.CharField(
        max_length=10
    )



