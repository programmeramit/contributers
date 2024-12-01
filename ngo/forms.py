# forms.py
from django import forms

class SetUsernameAndPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
