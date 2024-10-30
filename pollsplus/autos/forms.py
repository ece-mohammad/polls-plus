from django.forms import ModelForm, ValidationError

from autos.models import Auto


class AutoForm(ModelForm):
    class Meta:
        model = Auto
        fields = ("make", "nickname", "mileage", "comments")

    def __init__(self, *args, **kwargs):
        super(AutoForm, self).__init__(*args, **kwargs)
        self.fields['make'].widget.attrs['autofocus'] = True

    def clean_mileage(self):
        mileage = self.cleaned_data["mileage"]
        if mileage < 0:
            raise ValidationError("Mileage cannot be negative")
        return mileage
