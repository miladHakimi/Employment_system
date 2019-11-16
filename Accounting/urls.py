from django.conf.urls import url

from .views import EmployerViewSet, ApplicantViewSet, \
    UpdateAdView, PendingRequestsViewSet, \
    RejectedRequestsViewSet, AdViewSet, EditProfileViewSet, AppointmentViewSet

urlpatterns = [
    url(r'^$', EditProfileViewSet.as_view(), name='update-ad'),
    url(r'^ads/(?P<ad_id>\d+)/$', UpdateAdView.as_view(), name='update-ad'),
    url(r'^ads/', AdViewSet.as_view(), name='update-ad'),
    url(r'^applicants', ApplicantViewSet.as_view(), name='create-app'),
    url(r'^employers', EmployerViewSet.as_view(), name='create-emp'),
    url(r'^appointment', AppointmentViewSet.as_view(), name='view-app'),
    url(r'^pending', PendingRequestsViewSet.as_view(), name='view-pend'),
    url(r'^rejected', RejectedRequestsViewSet.as_view(), name='view-rej'),
]
