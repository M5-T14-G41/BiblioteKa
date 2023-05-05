from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


class CreateLoanView(CreateAPIView):
    # authentication_classes = []
    pass


class UpdateLoanView(RetrieveUpdateAPIView):
    pass
