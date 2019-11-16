from django.contrib import admin

# Register your models here.
from Commercial.models import Ad, Appointment

admin.site.register(Ad)
admin.site.register(Appointment)
