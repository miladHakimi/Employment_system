from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE

from Accounting.models import Applicant


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
            return Applicant.objects.create(**validated_data)
        except:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
