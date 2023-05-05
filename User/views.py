from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status

from User.permissions import UserAutentication
from .models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UsersSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


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

