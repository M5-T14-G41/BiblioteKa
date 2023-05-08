from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.generics import ListAPIView
from datetime import datetime as dt


from User.permissions import UserAutentication, IsAdmin
from .models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UsersSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from Loan.models import Loan
from Loan.serializers import LoanSerializer


class UserView(APIView):
    def get(self, request: Request) -> Response:
        user = User.objects.all()

        serializer = UsersSerializer(user, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    ...


class UserRetriverView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UserAutentication]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)
        serializer = UsersSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)
        serializer = UsersSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class RetrieveUserStatusView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request: Request, user_id: int) -> Response:
        user_loans = get_list_or_404(Loan, user_id=user_id, is_returned=False)
        serializer = LoanSerializer(user_loans, many=True)
        loans = [*serializer.data]
        not_returned = []
        user_status = {"banned": False}
        for loan in loans:
            convert_devolution_date = dt.strptime(loan["devolution_date"], "%Y-%m-%d")
            if dt.now() > convert_devolution_date:
                not_returned.append(loan)
                user_status["banned"] = True
                user_status["delayed_books"] = not_returned
        return Response(user_status, status.HTTP_200_OK)


class UserLoanView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request: Request, user_id: int) -> Response:
        user_loans = get_list_or_404(Loan, user_id=user_id)
        serializer = LoanSerializer(user_loans, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
