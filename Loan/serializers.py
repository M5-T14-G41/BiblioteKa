from rest_framework import serializers

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = [
            "user_id",
            "copy_id",
            "devolution_date",
            "is_returned",
        ]
