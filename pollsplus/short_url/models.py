from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.crypto import get_random_string
from simple_history.models import HistoricalRecords


class ShortURL(models.Model):
    MAX_SLUG_LEN: int = settings.MAX_SHORT_URL

    url = models.URLField(
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(3, "URL must be at least 3 characters long"),
        ]
    )
    slug = models.SlugField(max_length=MAX_SLUG_LEN, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(length=self.MAX_SLUG_LEN)
        super(ShortURL, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug
