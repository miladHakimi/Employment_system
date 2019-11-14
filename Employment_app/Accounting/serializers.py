from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE

from Accounting.models import Applicant, Employer
from Commercial.serializers import AdSerializer


class ApplicantSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        fields = (
            'firstName',
            'lastName',
            'username',
            'password',
            'age',
            'gender'

        )
        model = Applicant

    def create(self, validated_data):
        try:
            validated_data['password'] = make_password(validated_data['password'])
            return Applicant.objects.create(**validated_data)
        except:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)


class EmployerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    establishedYear = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    phone = serializers.CharField(max_length=11)

    class Meta:
        fields = (
            'companyName',
            'establishedYear',
            'username',
            'password',
            'address',
            'phone'
        )
        model = Employer

    # todo: length of the password

    def create(self, validated_data):
        try:
            validated_data['password'] = make_password(validated_data['password'])
            return Employer.objects.create(**validated_data)
        except:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)


class EmployerDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = (
            '__all__',
        )
