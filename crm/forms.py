# forms.py
from django import forms
from django.core.validators import MaxValueValidator
from multiupload.fields import MultiFileField
from .models import Client, Product, Category

class ClientForm(forms.ModelForm):
   
    class Meta:
        model = Client
        fields = '__all__'
        widgets ={
            'name' : forms.widgets.TextInput(attrs={"placeholder":"Client Name", "class":"form-control"}),
            'email' : forms.widgets.EmailInput(attrs={"placeholder":"Email", "class":"form-control"}),
            'phone_number' : forms.widgets.NumberInput(attrs={'class': 'form-control'}),
            'address' : forms.widgets.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
            'facebook' : forms.widgets.TextInput(attrs={'class' : 'form-control'}),
            'twitter' : forms.widgets.TextInput(attrs={'class' : 'form-control'}),
            'instagram' : forms.widgets.TextInput(attrs={'class' : 'form-control'}),
            'linkedin' : forms.widgets.TextInput(attrs={'class' : 'form-control'})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category','description', 'quantity_supplied','quantity_left', 'price', 'image']
        widgets ={
            'name' : forms.widgets.TextInput(attrs={"placeholder":"Product Name", "class":"form-control"}),
            'category' : forms.widgets.Select(attrs={'placeholder': 'Product Category', 'class': 'form-control'}),
            'image' : forms.widgets.FileInput(attrs={'class': 'form-control'}),
            'description' : forms.widgets.Textarea(attrs={'class' : 'form-control', 'rows': '5'}),
            'quantity_supplied' : forms.widgets.NumberInput(attrs={'placeholder': 'Quantity Supplied', 'class' : 'form-control'}),
            'quantity_left' : forms.widgets.NumberInput(attrs={'placeholder': 'Quantity Left', 'class' : 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_images': MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5),
        } 
        category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
        price = forms.DecimalField(validators=[MaxValueValidator(limit_value=2)])

