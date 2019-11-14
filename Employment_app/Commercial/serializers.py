from rest_framework import serializers

from Accounting.models import Employer, Applicant
from Commercial.models import Ad


class EmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = (
            'username',
        )


class AdSerializer(serializers.ModelSerializer):
    emp = EmpSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = (
            'id',
            'title',
            'emp',
            'expDate',
            'fieldsOfExpertise',
            'salary',
        )


class ApplySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(read_only=True)
    expDate = serializers.CharField(read_only=True)
    fieldsOfExpertise = serializers.CharField(read_only=True)
    salary = serializers.CharField(read_only=True)

    class Meta:
        model = Ad
        fields = (
            'id',
            'title',
            'expDate',
            'fieldsOfExpertise',
            'salary',
        )
