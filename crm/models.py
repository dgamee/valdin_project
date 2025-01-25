from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField

from django.utils.html import mark_safe

class DashboardItem(models.Model):
    class Meta:
        abstract = True


class Category(models.Model):
    category_id = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet='abcdefghijk1234567890')
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.category_id})
    def category_count(self):
        return Category.objects.count()

class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

class Client(models.Model):
    
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    facebook = models.CharField(max_length=35, unique=True, blank=True)
    twitter = models.CharField(max_length=35, unique=True, blank=True)
    instagram = models.CharField(max_length=35, unique=True, blank=True)
    linkedin = models.CharField(max_length=35, unique=True, blank=True)

    def __str__(self): 
        return f"{self.name} - {self.email} - {self.phone_number}"
    
    def client_count(self):
        return Client.objects.count()
    
    def get_absolute_url(self):
        return reverse("client_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True,  blank=True, upload_to='product_images')
    quantity_supplied = models.PositiveIntegerField()
    quantity_left = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    old_price = models.DecimalField(max_digits=999, decimal_places=2, default=1.99)
    date = models.DateTimeField(auto_now_add=True)
    date_updated =  models.DateTimeField(null=True, blank=True)

    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        
    def __str__(self):
        return self.name
    
    def discount(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_images')
    image = models.ImageField(upload_to='product_images/other/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image"
## a better way to handle product and image
#Product.objects.get(id=1).product_images

######################## CART, Order, OrderItems and Address ######################

class CartOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999, decimal_places=2, default= '1.99')
    payment_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    #product_status = models.CharField(choices=PRODUCT_CHOICE, max_length = 30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"



class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete= models.CASCADE)
    invoice_number = models.CharField(max_length=250)
    item = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=999, decimal_places=2)
    total = models.DecimalField(max_digits=999, decimal_places=2)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="media/%s" width="50" height="50" />' % (self.image.url))
