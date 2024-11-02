from django.forms import ModelForm, ValidationError
from django.utils.html import escape

from cats.models import Breed, Cat


class BreedForm(ModelForm):
    class Meta:
        model = Breed
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data["name"]
        if name == "":
            raise ValidationError("Name cannot be empty")
        return escape(name)


class CatForm(ModelForm):
    class Meta:
        model = Cat
        fields = "__all__"

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"]
        if nickname == "":
            raise ValidationError("Nickname cannot be empty")
        return escape(nickname)
