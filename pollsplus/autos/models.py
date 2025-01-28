from django.db import models
from django.core.validators import MinLengthValidator
from simple_history.models import HistoricalRecords

# Create your models here.
class Make(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Car's make (e.g. Ford)",
        validators=[MinLengthValidator(2, "Make must be at least 2 characters long")],
        blank=False,
        null=False,
        unique=True
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Auto(models.Model):
    make = models.ForeignKey(
        "Make",
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    nickname = models.CharField(
        max_length=200,
        help_text="Car's nickname (e.g. Focus)",
        validators=[MinLengthValidator(2, "Nickname must be at least 2 characters long")],
        blank=False
    )
    mileage = models.IntegerField()
    comments = models.TextField(blank=True, max_length=300)
    history = HistoricalRecords()

    def __str__(self):
        return self.nickname
