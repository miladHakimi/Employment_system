from django.contrib import admin
from .models import Applicant, Employer, MyUser

admin.site.register(MyUser)
admin.site.register(Applicant)
admin.site.register(Employer)

