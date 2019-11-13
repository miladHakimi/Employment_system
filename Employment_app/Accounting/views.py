from rest_framework import generics

from Accounting.serializers import ApplicantSerializer, EmployerSerializer


class ApplicantViewSet(generics.ListCreateAPIView):
    serializer_class = ApplicantSerializer
    queryset = ""


class EmployerViewSet(generics.ListCreateAPIView):
    serializer_class = EmployerSerializer
    queryset = ""
