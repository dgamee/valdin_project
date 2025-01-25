from django.urls import path

from .views import SignupPageView , LoginPageView 

urlpatterns = [
    path("signup/", SignupPageView.as_view(), name="signup"),
    path("login/", LoginPageView.as_view(), name="login"),
]