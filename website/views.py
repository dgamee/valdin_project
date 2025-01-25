from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin #login required to make page private
from django.views.decorators.cache import cache_control #Destroy the session after logout
from django.utils.decorators import method_decorator



# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AboutPageView(TemplateView):
    template_name = "about.html"

class ContactPageView(TemplateView):
    template_name = "contact.html"

class ServicePageView(TemplateView):
    template_name = "service.html"