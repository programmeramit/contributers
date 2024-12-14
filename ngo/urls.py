from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.generic import TemplateView  # new
urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"),name="home"),  # new
    path('donate/',views.donate,name="donate"),
    path('payment-success/<str:pay_id>', views.payment_success, name='payment_success'),
   

        path("accounts/", include("allauth.urls")), 

            path('group',views.request_group_membership,name="group")
            ]
