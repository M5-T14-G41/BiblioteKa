from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from User.models import User
from .models import Book
from .serializers import BookSerializer, CopySerializer
from rest_framework.views import APIView, Request, Response, status

from User.permissions import IsAdminOrReadOnly, IsAuthenticated

from .tasks import send_notification


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # def perform_create(self, serializer):
    #     serializer.save(book=self.request.data)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CopyCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = CopySerializer


class FollowingView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, book_id: int) -> Response:
        user_requester = request.user.id

        book = get_object_or_404(Book, id=book_id)
        user = get_object_or_404(User, id=user_requester)

        book.following.add(user)
        send_notification(user, book, "Following")
        return Response({"message": f"Você está seguindo o livro {book.name}!"}, status.HTTP_201_CREATED)


class GetFollowingView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request) -> Response:
        user = get_object_or_404(User, id=request.user.id)

        book_followed = Book.objects.filter(
            following=user
        )

        serializer = BookSerializer(book_followed, many=True)

        return Response({"user_id": user.id, "books_followed": serializer.data}, status.HTTP_200_OK)


class UnfollowView(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request: Request, book_id: int) -> Response:

        book = get_object_or_404(Book, id=book_id)
        user = get_object_or_404(User, id=request.user.id)

        book.following.remove(user)       
        send_notification(user, book, "unfollowing")

        return Response(status=status.HTTP_204_NO_CONTENT)