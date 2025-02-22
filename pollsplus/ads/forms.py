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
    max_upload_limit = settings.AD_PICTURE_MAX_SIZE
    max_upload_limit_text = _(f"{human_readable_size(max_upload_limit)}")

    class Meta:
        model = Ad
        fields = ('title', 'price', 'text', 'picture',)
