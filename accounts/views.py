from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm

# Create your views here.
class SignupPageView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("dashboard")


    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in
        login(self.request, self.object)
        # Add a success message
        messages.success(self.request, 'Signup successful! You are now logged in.')
        return response
    

class LoginPageView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add a custom welcome message
        messages.success(self.request, f'Welcome, {self.request.user}!')
        return response