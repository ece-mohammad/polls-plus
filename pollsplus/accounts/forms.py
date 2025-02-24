from allauth.account.forms import LoginForm
from django import forms
from copy import deepcopy

class CustomLoginForm(LoginForm):
    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class"      : "form-control textarea"
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        # Before passing data to the base form, adjust it.
        if 'data' in kwargs:
            data = deepcopy(kwargs['data'])
            data['login'] = deepcopy(data['username'])
            del kwargs['data']
            kwargs['data'] = data
            print(f">>>>>>>>>>>>>> {data=}")
        super().__init__(*args, **kwargs)
        # Optionally, hide the original login field if you're not rendering it.
        if 'login' in self.fields:
            self.fields['login'].widget = forms.HiddenInput()
