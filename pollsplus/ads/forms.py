from django.forms import ModelForm, ValidationError

from ads.models import AdComment

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
            raise ValidationError("Comment must be at least 2 characters long")
        return text
