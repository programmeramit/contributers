# signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(user_signed_up)
def redirect_after_signup(request, user, **kwargs):
    # Check if the user signed up via a social account
    if user.socialaccount_set.exists():
        return redirect('set_username_and_password')
