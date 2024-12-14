
# Create your models here.
from django.db import models
from django.contrib.auth.models import Group, User


class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donor_name} - ₹{self.amount}"



class PendingGroupRequest(models.Model):
    name = models.CharField(max_length=20,help_text="Enter your full name")
    phone_number = models.IntegerField(help_text="Enter your phone number",blank=True,null=True)
    email = models.EmailField(help_text="Enter your email",null=True,blank=True)
    password = models.CharField(max_length=20,help_text="Enter your password")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} requests to join"
