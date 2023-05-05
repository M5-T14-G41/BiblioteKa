from django.db import models
import datetime as dt


def generate_devolution_date():
    today = dt.date.today()
    next_week = today + dt.timedelta(days=8)

    while next_week.weekday() >= 5:
        next_week += dt.timedelta(days=1)
    return next_week


class Loan(models.Model):
    user_id = models.ForeignKey(
        "User.User",
        on_delete=models.CASCADE,
        related_name="loaned_for",
    )
    copy_id = models.ForeignKey(
        "Book.Copy",
        on_delete=models.CASCADE,
        related_name="copy_loaned",
    )
    devolution_date = generate_devolution_date()
    is_returned = models.BooleanField(default=False)
