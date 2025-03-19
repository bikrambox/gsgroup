# APIServer/forms.py
from django import forms

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            from django.contrib.auth import authenticate
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct email and password. Note that both fields may be case-sensitive."
                )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache