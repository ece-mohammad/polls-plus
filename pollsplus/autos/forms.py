from django.forms import ModelForm, ValidationError
from django.utils.html import escape

from autos.models import Auto, Make


class MakeForm(ModelForm):
    class Meta:
        model = Make
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super(MakeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    def clean_name(self):
        name = self.cleaned_data["name"]
        if name == "":
            raise ValidationError("Name cannot be empty")
        return escape(name)


class AutoForm(ModelForm):
    class Meta:
        model = Auto
        fields = ("make", "nickname", "mileage", "comments")

    def __init__(self, *args, **kwargs):
        super(AutoForm, self).__init__(*args, **kwargs)
        self.fields['make'].widget.attrs['autofocus'] = True

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"]
        if nickname == "":
            raise ValidationError("Nickname cannot be empty")
        return escape(nickname)

    def clean_comments(self):
        comments = self.cleaned_data["comments"]
        if comments == "":
            raise ValidationError("Comments cannot be empty")
        return escape(comments)

    def clean_mileage(self):
        mileage = self.cleaned_data["mileage"]
        if mileage < 0:
            raise ValidationError("Mileage cannot be negative")
        return mileage
