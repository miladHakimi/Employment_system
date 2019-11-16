from django.conf.urls import url

from .views import EmployerViewSet, ApplicantViewSet, \
    UpdateAdView, EmployerSetAppointmentViewSet, PendingRequestsViewSet, \
    RejectedRequestsViewSet, AcceptedRequestsViewSet, AdViewSet, EditProfileViewSet

urlpatterns = [
    url(r'^$', EditProfileViewSet.as_view(), name='update-ad'),
    url(r'^ads/(?P<ad_id>\d+)/$', UpdateAdView.as_view(), name='update-ad'),
    url(r'^ads/', AdViewSet.as_view(), name='update-ad'),
    url(r'^applicants', ApplicantViewSet.as_view(), name='create-app'),
    url(r'^employers', EmployerViewSet.as_view(), name='create-emp'),
    url(r'^set_appointment', EmployerSetAppointmentViewSet.as_view(), name='set-app'),
    url(r'^pending', PendingRequestsViewSet.as_view(), name='view-pend'),
    url(r'^rejected', RejectedRequestsViewSet.as_view(), name='view-rej'),
    url(r'^accepted', AcceptedRequestsViewSet.as_view(), name='view-acc'),
]
