from django.db import IntegrityError
from django.forms import ModelForm, ValidationError

from short_url.models import ShortURL


class ShortUrlForm(ModelForm):
    class Meta:
        model = ShortURL
        fields = ("url",)

    def clean_url(self):
        url = self.cleaned_data["url"]
        if url == "":
            raise ValidationError("URL cannot be empty")
        return url

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if commit:
    #         try:
    #             instance.save()
    #         except IntegrityError:
    #             pass
    #     return instance
