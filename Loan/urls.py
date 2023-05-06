from django.urls import path
from Loan.views import CreateLoanView, UpdateLoanView


urlpatterns = [
    path("loan/", CreateLoanView.as_view()),
    path("loan/update/", UpdateLoanView.as_view())
]
