from django.conf import settings
from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _

from ads.models import Ad, AdComment
from utils.helpers import human_readable_size

__all__ = (
    'AdCommentForm',
)


class AdCommentForm(ModelForm):
    class Meta:
        model = AdComment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 2:
            raise ValidationError(
                _("Comment must be at least 2 characters long")
            )
        return text


class AdForm(ModelForm):
    max_upload_limit = settings.AD_IMAGE_MAX_SIZE
    max_upload_limit_text = _(f"{human_readable_size(max_upload_limit)}")

    class Meta:
        model = Ad
        fields = ('title', 'price', 'text', 'image',)

    def clean_image(self):
        image = self.cleaned_data['image']
        if image is False and self.instance.image:
            self.instance.image.delete()

        elif image:
            if image == self.instance.image:
                return self.instance.image
            else:
                self.instance.image.delete()

        return image
