from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name","last_name","email","username","password1","password2")

        widgets ={
            'first_name' : forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}),
            'last_name' : forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}),
            'email' : forms.widgets.EmailInput(attrs={"placeholder":"Email", "class":"form-control"}),
            'username' : forms.widgets.TextInput(attrs={"placeholder":"Username", "class":"form-control"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({"placeholder": "Password", "class": "form-control"})
        self.fields['password2'].widget.attrs.update({"placeholder": "Confirm Password", "class": "form-control"})
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name","last_name","email","username",)