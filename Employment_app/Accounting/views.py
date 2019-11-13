from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

from Accounting.serializers import ApplicantSerializer
from .models import Applicant, Employer


class ApplicantViewSet(generics.ListCreateAPIView):
    """User ViewSet"""

    serializer_class = ApplicantSerializer
    queryset = ""

    # def get(self, request, format=None):
    #     # usernames = [user.username for user in User.objects.all()]
    #     return Response({'status_code': 400}, status=status.HTTP_201_CREATED)
