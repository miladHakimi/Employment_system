from django.conf.urls import url

from .views import EmployerViewSet, ApplicantViewSet, ApplicantDashboardView, EmployerDashboardViewSet, MakeAdViewSet, \
    UpdateAdView

urlpatterns = [
    url(r'^ads/(?P<ad_id>\d+)/$', UpdateAdView.as_view(), name='update-ad'),
    url(r'^create/applicant', ApplicantViewSet.as_view(), name='create-app'),
    url(r'^create/employer', EmployerViewSet.as_view(), name='create-emp'),
    url(r'^view_ads', ApplicantDashboardView.as_view(), name='view-ads'),
    url(r'^employer_dashboard', EmployerDashboardViewSet.as_view(), name='dashboard'),
    url(r'^make_ad', MakeAdViewSet.as_view(), name='make-ad'),
]
