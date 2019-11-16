import re

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Accounting.models import Employer, Applicant
from Accounting.serializers import ApplicantSerializer, EmployerSerializer, RequestSerializer, AppointmentSerializer, \
    PendingRequestSerializer, ApplicantAppointmentSerializer, ApplicantEditSerializer, EmployerEditSerializer
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


class AdViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_employer():
            return Employer.objects.get(id=self.request.user.id).ads
        elif self.request.user.is_applicant():
            id_list = Request.objects.filter(applicant=self.request.user).values_list('ad_id', flat=True)
            return Ad.objects.all().exclude(id__in=id_list)

    def get_serializer_class(self):
        if self.request.user.is_applicant():
            return ApplySerializer
        if self.request.user.is_employer():
            return AdSerializer
        return None

    def post(self, request, *args, **kwargs):
        if self.request.user.is_employer():
            return self.make_ad(request, args, kwargs)
        elif self.request.user.is_applicant():
            return self.apply_for_ad(request, args, kwargs)
        else:
            return Response({'detail': 'Unauthorised user'}, status=status.HTTP_401_UNAUTHORIZED)

    def apply_for_ad(self, request, *args, **kwargs):
        if not self.request.user.is_applicant():
            return Response({'detail': 'Unauthorised user'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            ad = Ad.objects.get(id=request.data.get('id'))
            app = Applicant.objects.get(id=self.request.user.id)
            if ad.id in app.request.values_list('ad_id', flat=True):
                return Response({'detail': 'You have already submitted for this ad.'},
                                status=status.HTTP_400_BAD_REQUEST)

            Request.objects.create(ad=ad, applicant=app)
            return Response(self.get_serializer_class()(ad).data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

    def make_ad(self, request, *args, **kwargs):
        if not self.request.user.is_employer():
            return Response({'detail': 'Unauthorised user'}, status=status.HTTP_401_UNAUTHORIZED)
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


class UpdateAdView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdSerializer

    def get(self, request, ad_id):
        ad = Ad.objects.get(id=ad_id)
        serializer = AdSerializer(ad)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        ad_id = kwargs['ad_id']
        ad = Ad.objects.get(id=ad_id)
        data = self.serializer_class(data=self.request.data)

        if data.is_valid(raise_exception=True):
            if ad.employer.id != self.request.user.id:
                return Response({'details': 'You do not have access to this ad.'}, status.HTTP_401_UNAUTHORIZED)

        try:
            ad.title = data.data['title']
            ad.expDate = data.data['expDate']
            ad.fieldsOfExpertise = data.data['fieldsOfExpertise']
            ad.salary = data.data['salary']
            ad.save()
            return Response(self.serializer_class(ad).data, status.HTTP_202_ACCEPTED)

        except:
            return Response({'details': 'Form data is not valid.'}, status.HTTP_400_BAD_REQUEST)


class EmployerRequestReviewViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.filter(ad__employer_id=self.request.user.id, rejected=False, accepted=False)

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
        return Appointment.objects.filter(employer_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_employer():
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
            return Response({'detail': 'You have handled this request before.'}, status=status.HTTP_400_BAD_REQUEST)
        req.accepted = True
        try:
            Appointment.objects.create(employer_id=self.request.user.id, applicant=req.applicant, date=date)
            req.save()
            return Response({'detail': 'submitted successfully'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'detail': 'Input format is not valid.'}, status=status.HTTP_400_BAD_REQUEST)


class PendingRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PendingRequestSerializer

    def get_queryset(self):
        if self.request.user.is_employer():
            return Request.objects.filter(ad__employer_id=self.request.user.id, rejected=False, accepted=False)
        elif self.request.user.is_applicant():
            return Request.objects.filter(applicant_id=self.request.user.id, rejected=False, accepted=False)
        return None


class RejectedRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PendingRequestSerializer

    def get_queryset(self):
        if self.request.user.is_employer():
            return Request.objects.filter(ad__employer_id=self.request.user.id, rejected=True)
        elif self.request.user.is_applicant():
            return Request.objects.filter(applicant_id=self.request.user.id, rejected=True)
        return None


class AcceptedRequestsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApplicantAppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_employer():
            return Appointment.objects.filter(employer_id=self.request.user.id)
        elif self.request.user.is_applicant():
            return Request.objects.filter(ad__employer_id=self.request.user.id)
        return None


class EditProfileViewSet(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        self.request.user = Employer.objects.get(username="c")
        if self.request.user.is_applicant():
            return ApplicantEditSerializer
        elif self.request.user.is_employer():
            return EmployerEditSerializer
        return ApplicantEditSerializer

    def get_queryset(self):
        self.request.user = Employer.objects.get(username="c")
        if self.request.user.is_employer():
            return Employer.objects.filter(id=self.request.user.id)
        if self.request.user.is_applicant():
            return Applicant.objects.filter(id=self.request.user.id)
        else:
            return None

    def post(self, request, *args, **kwargs):
        self.request.user = Employer.objects.get(username="c")

        if self.request.user.is_employer():
            return self.update_emp(request, *args, **kwargs)
        if self.request.user.is_applicant():
            return self.update_app(request)

    def update_emp(self, request, *args, **kwargs):
        emp = Employer.objects.get(id=self.request.user.id)
        fields = emp.fieldsOfExpertise
        exp = request.data.get('fieldsOfExpertise')
        if exp is not None:
            fields.append(exp)

        if exp in self.request.user.fieldsOfExpertise:
            return Response({'details': 'You have already added this to your fields.'}, status.HTTP_400_BAD_REQUEST)
        try:
            emp.fieldsOfExpertise = fields
            emp.save()
            return Response({'details': 'user updated'}, status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Inputs are not valid'}, status.HTTP_400_BAD_REQUEST)

    def update_app(self, request):
        app = Applicant.objects.get(id=self.request.user.id)
        fields = app.fieldsOfExpertise
        cv = app.cv
        phone = app.phone

        exp = request.data.get('fieldsOfExpertise')
        newCv = request.data.get('cv')
        new_phone = request.data.get('phone')

        if exp in self.request.user.fieldsOfExpertise:
            return Response({'details': 'You have already added this to your fields.'}, status.HTTP_400_BAD_REQUEST)

        if exp is not None:
            fields.append(exp)

        if newCv is not None:
            cv = newCv

        if new_phone is not None:
            phone = new_phone

        try:
            app.phone = phone
            app.fieldsOfExpertise = fields
            app.cv = cv
            app.full_clean()
            app.save()
            return Response({'details': 'user updated'}, status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Inputs are not valid'}, status.HTTP_400_BAD_REQUEST)
