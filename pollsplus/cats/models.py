from django.core.validators import MinLengthValidator
from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.
class Breed(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        validators=[
            MinLengthValidator(
                2,
                "Breed must be at least 2 characters long"
            )
        ]
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Cat(models.Model):
    breed = models.ForeignKey("Breed", on_delete=models.CASCADE)
    nickname = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        validators=[
            MinLengthValidator(
                2,
                "Nickname must be at least 2 characters long"
            )
        ]
    )
    weight = models.PositiveIntegerField()
    foods = models.CharField(max_length=200)
    history = HistoricalRecords()

    def __str__(self):
        return self.nickname
