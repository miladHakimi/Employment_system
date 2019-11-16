import re

import django_filters
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Accounting.models import Employer, Applicant
from Accounting.serializers import ApplicantSerializer, EmployerSerializer, RequestSerializer, AppointmentSerializer, \
    PendingRequestSerializer, ApplicantAppointmentSerializer
from Commercial.models import Ad, Request, Appointment
from Commercial.serializers import AdSerializer, ApplySerializer

FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(name):
    s = FIRST_CAP_RE.sub(r'\1_\2', name)
    return ALL_CAP_RE.sub(r'\1_\2', s).lower()


class RequestValidationError(object):
    pass


def get_required_fields(request, field_keys):
    data = {}
    for key in field_keys:
        field = request.data.get(key)
        if not field:
            raise RequestValidationError
        data[camel_to_snake(key)] = field
    return data


class ApplicantViewSet(generics.ListCreateAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return None


class EmployerViewSet(generics.ListCreateAPIView):
    serializer_class = EmployerSerializer
    permission_classes = [AllowAny, ]
    queryset = ""


class UserFilter(django_filters.FilterSet):
    LOOK_UP_CHOICES = [('prog', 'Programmer'), ('mech', 'Mechanical Engineer'),
                       ('metal', 'Metak Engineer')]

    field = django_filters.ChoiceFilter(
        choices=LOOK_UP_CHOICES,
        field_name='fieldsOfExpertise',
        lookup_expr='exact',
    )

    class Meta:
        model = Ad
        fields = ['field']


class ApplicantDashboardView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ApplySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_applicant():
            return Response({'detail': 'Unauthorised user'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            ad = Ad.objects.get(id=request.data.get('id'))
            app = Applicant.objects.get(id=self.request.user.id)
            if ad.id in app.request.values_list('ad_id', flat=True):
                return Response({'detail': 'You have already submitted for this ad.'},
                                status=status.HTTP_400_BAD_REQUEST)

            Request.objects.create(ad=ad, applicant=app)
            return Response(self.serializer_class(ad).data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        id_list = Request.objects.filter(applicant=self.request.user).values_list('ad_id', flat=True)
        queryset = Ad.objects.all().exclude(id__in=id_list)
        return queryset


class MakeAdViewSet(generics.ListCreateAPIView):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'emp':
            return self.request.user.ads
        else:
            return None

    def post(self, request, *args, **kwargs):
        try:
            title = request.data.get('title')
            date = request.data.get('expDate')
            expertise = request.data.get('fieldsOfExpertise')
            salary = request.data.get('salary')
            user = Employer.objects.get(id=self.request.user.id)

            Ad.objects.create(title=title, expDate=date, fieldsOfExpertise=expertise, salary=salary, employer=user)
            return Response({'detail': 'created'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'detail': 'inputs are not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        return self.request.user


#
class UpdateAdView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdSerializer

    def get(self, request, ad_id):
        ad = Ad.objects.get(id=ad_id)
        serializer = AdSerializer(ad)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        ad_id = kwargs['ad_id']
        data = self.serializer_class(data=self.request.data)

        if data.is_valid(raise_exception=True):
            ad = Ad.objects.get(id=ad_id)
            if ad.employer.id != self.request.user.id:
                return Response({'status': 'You do not have access to this ad.'}, status.HTTP_401_UNAUTHORIZED)

            ad.title = data.data['title']
            ad.expDate = data.data['expDate']
            ad.fieldsOfExpertise = data.data['fieldsOfExpertise']
            ad.salary = data.data['salary']
            ad.save()

            return Response(self.serializer_class(ad).data, status.HTTP_202_ACCEPTED)

        return Response({'status': 'Form data is not valid.'}, status.HTTP_400_BAD_REQUEST)


class EmployerRequestReviewViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.filter(ad__employer=self.request.user, rejected=False, accepted=False)

    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id')
            req = Request.objects.get(id=id)
            date = request.data.get('date')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.request.user.id != req.ad.employer.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        req.rejected = True
        req.save()

        return Response({'remaining ads': self.get_queryset()}, status=status.HTTP_202_ACCEPTED)


class EmployerSetAppointmentViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(employer=self.request.user)

    def post(self, request, *args, **kwargs):
        if self.request.user.user_type != 'emp':
            return Response({'detail': 'You do not have access to this page.'}, status=status.HTTP_401_UNAUTHORIZED)
        date = ""
        try:
            id = request.data.get('id')
            req = Request.objects.get(id=id)
            date = request.data.get('date')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.request.user.id != req.ad.employer.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if req.accepted or req.rejected:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        req.accepted = True
        req.save()
        Appointment.objects.create(employer=self.request.user, applicant=req.applicant, date=date)
        return Response(status=status.HTTP_201_CREATED)


class PendingRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PendingRequestSerializer

    def get_queryset(self):
        return Request.objects.filter(applicant_id=self.request.user.id, rejected=False, accepted=False)


class RejectedRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PendingRequestSerializer

    def get_queryset(self):
        return Request.objects.filter(applicant_id=self.request.user.id, rejected=True)


class AcceptedRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApplicantAppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(applicant_id=self.request.user.id)
