from django import forms
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
    )
    password = forms.CharField(
    )

class AddForm (forms.Form):
    a = forms.CharField(widget=forms.Textarea)