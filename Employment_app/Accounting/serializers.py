from rest_framework import serializers
from Accounting.models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'firstName',
            'lastName',
            'userName',
            'age',

        )
        model = Applicant
