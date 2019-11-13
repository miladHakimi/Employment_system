from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE

from Accounting.models import Applicant, Employer


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
            'userName',
            'password',
            'age',
            'gender'

        )
        model = Applicant

    # todo: user and pass not the same

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

    class Meta:
        fields = (
            'companyName',
            'establishedYear',
            'userName',
            'password',
            'address',
            'phone'

        )
        model = Employer

    # todo: user and pass not the same

    def create(self, validated_data):
        try:
            validated_data['password'] = make_password(validated_data['password'])
            return Employer.objects.create(**validated_data)
        except:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
