from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("registerUser/", views.registerUser, name="registerUser"),
    path("registerVendor/", views.registerVendor, name="registerVendor"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("custDashboard/", views.custDashboard, name="custDashboard"),
    path("vendorDashboard/", views.vendorDashboard, name="vendorDashboard"),
    path("MyAccount", views.MyAccount, name="MyAccount"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path("reset_password_validation/<uidb64>/<token>/", views.reset_password_validation, name="reset_password_validation"),
    path("reset_password/", views.reset_password, name="reset_password"),
]