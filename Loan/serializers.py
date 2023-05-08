from rest_framework import serializers
from rest_framework.views import Response, status
from rest_framework.validators import ValidationError
from django.shortcuts import get_list_or_404
from datetime import datetime as dt
from django.forms.models import model_to_dict


from .models import Loan
from User.models import User


class LoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_loans = Loan.objects.filter(user_id=validated_data["user_id"], is_returned=False)
        copy_loans = Loan.objects.filter(copy_id=validated_data["copy_id"], is_returned=False).exists()
        not_returned = []
        user_status = {"banned": False}
        
        if copy_loans:
            raise ValidationError({"message": "This copy has already been loaned"})

        for loan in user_loans:
            convert_devolution_date = dt.strptime(str(loan.devolution_date), "%Y-%m-%d")
            if dt.now() > convert_devolution_date:
                not_returned.append(model_to_dict(loan))
                user_status["banned"] = True
                user_status["delayed_copies"] = not_returned

        if user_status["banned"] is True:
            raise ValidationError(user_status)
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
        
