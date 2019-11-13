from django.conf.urls import url

from .views import EmployerViewSet, ApplicantViewSet

urlpatterns = [
    url(r'^create/applicant', ApplicantViewSet.as_view()),
    url(r'^create/employer', EmployerViewSet.as_view()),

]
