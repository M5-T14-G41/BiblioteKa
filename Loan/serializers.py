from rest_framework import serializers

from .models import Loan
from User.models import User


class LoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_id = validated_data["user_id"]
        user = User.objects.get(id=user_id)
        print(user)
        if user["is_banned"]:
            return {"message": "This user is banned"}
        return Loan.objects.create(**validated_data)

    class Meta:
        model = Loan
        fields = [
            "user_id",
            "copy_id",
            "devolution_date",
            "is_returned",
        ]

