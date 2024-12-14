# forms.py
from django import forms
from .models import PendingGroupRequest

class SetUsernameAndPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class UserForm(forms.ModelForm):
    class Meta:
        model= PendingGroupRequest
        fields = ["name","password","phone_number","email"]
