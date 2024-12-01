from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.generic import TemplateView  # new
urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"),name="home"),  # new
    path('donate/',views.donate),
    path('payment-success/<str:pay_id>', views.payment_success, name='payment_success'),
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/donations', views.admin_dashboard_donations, name='admin_dashboard_donations'),

    path('logout/', views.admin_logout, name='admin_logout'),
        path("accounts/", include("allauth.urls")), 

            path('set-username-password/', views.set_username_and_password, name='set_username_and_password'),
            ]
