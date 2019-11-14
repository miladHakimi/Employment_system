from django.conf.urls import url

from .views import EmployerViewSet, ApplicantViewSet, ApplicantDashboardView, EmployerDashboardViewSet, MakeAdViewSet, \
    UpdateAdView

urlpatterns = [
    url(r'^ads/(?P<ad_id>\d+)/$', UpdateAdView.as_view(), name='office-meetings'),
    url(r'^create/applicant', ApplicantViewSet.as_view()),
    url(r'^create/employer', EmployerViewSet.as_view(), name='emp_create'),
    url(r'^change_name', ApplicantDashboardView.as_view(), name='change_name'),
    url(r'^employer_dashboard', EmployerDashboardViewSet.as_view(), name='dashboard'),
    url(r'^make_ad', MakeAdViewSet.as_view(), name='make_add'),
]
