from rest_framework import serializers
from rest_framework.views import Response, status
from rest_framework.validators import ValidationError

from .models import Loan
from User.models import User


class LoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_verify = User.objects.get(username=validated_data["user_id"])
        if user_verify.is_banned:
            raise ValidationError({"message": "This user is banned"})
        return Loan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "is_returned":
                setattr(instance, key, value)
            instance.save()
        return instance

    class Meta:
        model = Loan
        fields = [
            "user_id",
            "copy_id",
            "devolution_date",
            "is_returned",
        ]
        
