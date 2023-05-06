from django.urls import path
from .views import UserView, UserRetriverView, RetrieveUserStatusView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:user_id>/", UserRetriverView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("users/status/<int:user_id>/", RetrieveUserStatusView.as_view()),
    
]