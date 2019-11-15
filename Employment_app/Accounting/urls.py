
from django.conf.urls import url

from .views import EmployerViewSet, ApplicantViewSet, ApplicantDashboardView, EmployerDashboardViewSet, MakeAdViewSet, \
    UpdateAdView, EmployerRequestReviewViewSet, EmployerSetAppointmentViewSet, PendingRequestsViewSet, \
    RejectedRequestsViewSet, AcceptedRequestsViewSet, GetUserNameViewSet

urlpatterns = [
    url(r'^ads/(?P<ad_id>\d+)/$', UpdateAdView.as_view(), name='update-ad'),
    url(r'^create/applicant', ApplicantViewSet.as_view(), name='create-app'),
    url(r'^create/employer', EmployerViewSet.as_view(), name='create-emp'),
    url(r'^view_ads', ApplicantDashboardView.as_view(), name='view-ads'),
    url(r'^employer_dashboard', EmployerDashboardViewSet.as_view(), name='dashboard'),
    url(r'^make_ad', MakeAdViewSet.as_view(), name='make-ad'),
    url(r'^req_list', EmployerRequestReviewViewSet.as_view(), name='list-apps'),
    url(r'^set_appointment', EmployerSetAppointmentViewSet.as_view(), name='set-app'),
    url(r'^view_pending', PendingRequestsViewSet.as_view(), name='view-pend'),
    url(r'^view_rejected', RejectedRequestsViewSet.as_view(), name='view-rej'),
    url(r'^view_accepted', AcceptedRequestsViewSet.as_view(), name='view-acc'),
    url(r'^status', GetUserNameViewSet.as_view(), name='user-stat'),
]
