import re

import django_filters
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Accounting.models import Applicant, Employer, User
from Accounting.serializers import ApplicantSerializer, EmployerSerializer, EmployerDashboardSerializer, \
    RequestSerializer, AppointmentSerializer, PendingRequestSerializer, ApplicantAppointmentSerializer
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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        print("user = " + self.request.user.username)
        return Applicant.objects.all()


class EmployerViewSet(generics.ListCreateAPIView):
    serializer_class = EmployerSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = ""


class UserFilter(django_filters.FilterSet):
    LOOK_UP_CHOICES = [('programming', 'Programmer'), ('mechanical_engineering', 'Mechanical Engineer')]

    field = django_filters.ChoiceFilter(
        choices=LOOK_UP_CHOICES,
        field_name='fieldsOfExpertise',
        lookup_expr='exact',
    )

    class Meta:
        model = Ad
        fields = ['field']


def get_user():
    return Applicant.objects.get(username="2")


def get_id_list(user):
    id_list = Request.objects.filter(applicant=user).values_list('ad_id', flat=True)
    return id_list


class ApplicantDashboardView(generics.ListCreateAPIView):
    queryset = Ad.objects.all().exclude(id__in=get_id_list(get_user()))
    serializer_class = ApplySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def post(self, request, *args, **kwargs):
        self.user = Applicant.objects.get(username="2")
        ad = Ad.objects.get(id=request.data.get('id'))
        user = self.user
        req = Request(ad=ad, applicant=user)
        req.save()
        return Response(self.serializer_class(ad).data, status=status.HTTP_202_ACCEPTED)


class EmployerDashboardViewSet(generics.ListCreateAPIView):
    serializer_class = EmployerDashboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.request.user = Employer.objects.filter(username="3")[0]
        if not self.request.user.is_anonymous:
            return Employer.objects.filter(username=self.request.user.username)
        return None

    def get_object(self):
        return self.request.user


class MakeAdViewSet(generics.ListCreateAPIView):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.request.user = Employer.objects.filter(username="3")[0]
        if not self.request.user.is_anonymous:
            return Employer.objects.filter(username="3")[0].ads
        return None

    def post(self, request, *args, **kwargs):
        try:
            self.request.user = Employer.objects.filter(username="3")[0]

            title = request.data.get('title')
            date = request.data.get('expDate')
            expertise = request.data.get('fieldsOfExpertise')
            salary = request.data.get('salary')
            user = Employer.objects.filter(username="3")[0]
            p = Ad(title=title, expDate=date, fieldsOfExpertise=expertise, salary=salary, employer=user)
            p.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        return self.request.user


#
class UpdateAdView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdSerializer
    user = ""

    def get(self, request, ad_id):
        self.user = User.objects.get(username="3")
        ad = Ad.objects.get(id=ad_id)
        serializer = AdSerializer(ad)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user_id = kwargs['ad_id']
        data = self.serializer_class(data=self.request.data)

        if data.is_valid(raise_exception=True):
            ad = Ad.objects.get(id=user_id)
            ad.title = data.data['title']
            ad.expDate = data.data['expDate']
            ad.fieldsOfExpertise = data.data['fieldsOfExpertise']
            ad.salary = data.data['salary']
            if ad.employer.id != self.user.id:
                return Response({'status': 'You do not have access to this ad.'}, status.HTTP_401_UNAUTHORIZED)
            ad.save()
            return Response(self.serializer_class(ad).data, status.HTTP_202_ACCEPTED)

        return Response({'status': 'Form data is not valid.'}, status.HTTP_400_BAD_REQUEST)


class EmployerRequestReviewViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RequestSerializer
    user = ""

    def get_queryset(self):
        self.user = Employer.objects.get(username="3")
        return Request.objects.filter(ad__employer=self.user, rejected=False, accepted=False)

    def post(self, request, *args, **kwargs):
        self.user = Employer.objects.get(username="3")
        try:
            id = request.data.get('id')
            req = Request.objects.get(id=id)
            date = request.data.get('date')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.user.id != req.ad.employer.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        req.rejected = True
        req.save()

        return Response({'remaining ads': self.get_queryset()}, status=status.HTTP_202_ACCEPTED)


class EmployerSetAppointmentViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    user = ""

    def get_queryset(self):
        self.user = Employer.objects.get(username="3")
        return Appointment.objects.filter(employer=self.user)

    def post(self, request, *args, **kwargs):
        self.user = Employer.objects.get(username="3")
        date = ""
        try:
            id = request.data.get('id')
            req = Request.objects.get(id=id)
            date = request.data.get('date')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.user.id != req.ad.employer.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if req.accepted or req.rejected:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        req.accepted = True
        req.save()
        Appointment.objects.create(employer=self.user, applicant=req.applicant, date=date)
        return Response(status=status.HTTP_201_CREATED)


class PendingRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PendingRequestSerializer
    user = ""

    def get_queryset(self):
        self.user = Applicant.objects.get(username="2")
        return Request.objects.filter(applicant=self.user, rejected=False, accepted=False)


class RejectedRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PendingRequestSerializer
    user = ""

    def get_queryset(self):
        self.user = Applicant.objects.get(username="2")
        return Request.objects.filter(applicant=self.user, rejected=True)


class AcceptedRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApplicantAppointmentSerializer
    user = ""

    def get_queryset(self):
        self.user = Applicant.objects.get(username="2")
        return Appointment.objects.filter(applicant=self.user)


class ProductList(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fieldsOfExpertise']
