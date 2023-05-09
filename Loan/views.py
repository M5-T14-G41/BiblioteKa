from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from Book.models import Copy
from Book.tasks import send_notification
from User.models import User
from User.permissions import IsAdminOrReadOnly, IsAdmin
from Loan.serializers import LoanSerializer
from Loan.models import Loan

from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView, Request, Response, status
from datetime import datetime as dt

from Loan.models import generate_devolution_date


class CreateLoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    serializer_class = LoanSerializer


class UpdateLoanView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    lookup_url_kwarg = "loan_id"

    def partial_update(self, request: Request, loan_id: int,  *args, **kwargs):
        kwargs['partial'] = True

        user_id = get_object_or_404(Loan, id=loan_id).user_id.id

        loan = get_object_or_404(Loan, id=loan_id)

        copy = get_object_or_404(Copy, id=loan.copy_id.id)
        copy.isBorrowed = False
        copy.save()

        book = model_to_dict(copy.book)

        copies = [model_to_dict(c) for c in Copy.objects.filter(
            book=book["id"], isBorrowed=False)]

        for user in book["following"]:
            if copies.__len__() > 0:
                send_notification(user, copy.book, "isavaliable")

        user = get_object_or_404(User, id=user_id)

        if loan.devolution_date:
            convert_devolution_date = dt.strptime(
                f"{loan.devolution_date}", "%Y-%m-%d")

        if dt.now() < convert_devolution_date:
            user.is_banned = generate_devolution_date()
            user.save()

        return self.update(request, *args, **kwargs)
