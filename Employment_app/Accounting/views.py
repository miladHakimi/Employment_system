import re

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Accounting.models import Applicant, Employer
from Accounting.serializers import ApplicantSerializer, EmployerSerializer, EmployerDashboardSerializer
from Commercial.models import Ad
from Commercial.serializers import AdSerializer

FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(name):
    """Turns camel case to snake case"""

    s = FIRST_CAP_RE.sub(r'\1_\2', name)
    return ALL_CAP_RE.sub(r'\1_\2', s).lower()


class RequestValidationError(object):
    pass


def get_required_fields(request, field_keys):
    """Returns required fields"""

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


class ApplicantDashboardView(APIView):
    """Remove User Avatar View"""

    def get(self, request):
        """Removes user avatar"""

        try:
            request.user.firstName = "mili"
            request.user.save()
            return Response({
                'status': 'OK',
            })
        except:
            return Response({
                'status': 'NOK',
                'error': 'removing failed',
            })


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
            return Employer.objects.filter(username=self.request.user.username)[0].ads
        return None

    def post(self, request, *args, **kwargs):
        self.request.user = Employer.objects.filter(username="3")[0]

        title = request.data.get('title')
        date = request.data.get('expDate')
        expertise = request.data.get('fieldsOfExpertise')
        salary = request.data.get('salary')
        user = Employer.objects.filter(username="3")[0]
        p = Ad(title=title, expDate=date, fieldsOfExpertise=expertise, salary=salary, employer=user)
        p.save()
        return Response({'status': 'ok'})

    def get_object(self):
        return self.request.user
