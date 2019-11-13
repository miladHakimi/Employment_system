from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

from Accounting.serializers import ApplicantSerializer
from .models import Applicant, Employer


class ApplicantViewSet(generics.ListCreateAPIView):
    """User ViewSet"""

    serializer_class = ApplicantSerializer
    queryset = Applicant.objects.all()
    # def create(self, request, **kwargs):
    #     try:
    #         newApplicant = Applicant(
    #             firstName=request.data.get('first_name'),
    #             lastName=request.data.get('last_name'),
    #             userName=request.data.get('user_name'),
    #             age=request.data.get('age'),
    #             gender=request.data.get('gender'),
    #             phone=request.data.get('phone'),
    #         )
    #         newApplicant.set_password(request.data.get('password'))
    #         newApplicant.save()
    #         return Response({
    #             'status_code': 200,
    #             'detail': 'User created successfully.'
    #         })
    #     except:
    #         return Response({
    #             'status_code': 405,
    #             'detail': 'Creating user failed.'
    #         })

    def get(self, request, format=None):
        # usernames = [user.username for user in User.objects.all()]
        return Response({'status_code': 400}, status=status.HTTP_201_CREATED)
    # def update(self, request, pk):
    #     if request.user.is_anonymous:
    #         return Response({
    #             'status': 'NOK',
    #             'error': {
    #                 'code': 400,
    #                 'message': 'You are not logged in.',
    #             },
    #         })
    #     try:
    #         if request.data.get('first_name'):
    #             request.user.first_name = request.data.get('first_name')
    #         if request.data.get('last_name'):
    #             request.user.last_name = request.data.get('last_name')
    #         if request.data.get('phone'):
    #             request.user.phone = request.data.get('phone')
    #         request.user.full_clean()
    #         request.user.save()
    #         if request.data.get('old_password') is not None and \
    #             request.data.get('new_password') is not None:
    #             if request.user.check_password(request.data.get('old_password')):
    #                 request.user.set_password(request.data.get('new_password'))
    #                 request.user.full_clean()
    #                 request.user.save()
    #                 return Response({
    #                     'status': 'OK',
    #                     'message': 'Password successfully updated.',
    #                 })
    #             return Response({
    #                 'status': 'NOK',
    #                 'error': {
    #                     'code': 401,
    #                     'message': 'Provided password is incorrect.',
    #                 },
    #             })
    #         return Response({
    #             'status': 'OK',
    #             'message': 'User updated successfully.',
    #         })
    #     except:
    #         return Response({
    #             'status': 'NOK',
    #             'error': {
    #                 'code': 402,
    #                 'message': 'Updating failed.',
    #             },
    #         })

    def get_object(self):
        return self.request.user
