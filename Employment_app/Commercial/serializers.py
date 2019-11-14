from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from Accounting.models import Employer
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
