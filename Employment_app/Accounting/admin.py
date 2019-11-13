from django.contrib import admin
from .models import Applicant, Employer, User

admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Employer)

