from . import views

from django.urls import path

urlpatterns = [
    path("book/", views.BookView.as_view()),
    path("book/<int:pk>/", views.BookDetailView.as_view()),
    path("copy/", views.CopyCreateView.as_view()),
    path("following/", views.GetFollowingView.as_view()),
    path("books/<int:book_id>/follow/", views.FollowingView.as_view()),
    path("unfollow/<int:book_id>/", views.UnfollowView.as_view()),
]
