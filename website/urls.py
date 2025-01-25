from django.urls import path
from .views import HomePageView, AboutPageView, DashboardPageView, ServicePageView, ContactPageView


urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("service/", ServicePageView.as_view(), name="service"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("landing/", DashboardPageView.as_view(), name="dashboard"),
    path("", HomePageView.as_view(), name="home"),
]
