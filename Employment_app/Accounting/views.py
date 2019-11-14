import re

from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Accounting.models import Applicant, Employer, User
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


class UpdateAdView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdSerializer
    user = User.objects.get(username="3")

    def get(self, request, ad_id):
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
