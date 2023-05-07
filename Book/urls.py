from django.urls import path

from .views import BookView, BookDetailView, CopyCreateView

urlpatterns = [
    path("book/", BookView.as_view()),
    path("book/<int:pk>/", BookDetailView.as_view()),
    path("copy/", CopyCreateView.as_view())
]
