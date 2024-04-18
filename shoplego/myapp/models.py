from datetime import date, datetime
from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    name_user = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    position = models.CharField(max_length=20, default='khach_hang')

class Product(models.Model):
    id_product = models.AutoField(primary_key=True)  # Trường khóa chính tùy chỉnh
    name_product = models.CharField(max_length=100)
    img_product = models.ImageField(upload_to='product_images/', null=False, default=None)
    description = models.TextField()
    price = models.TextField()
    quantity = models.IntegerField()

class Cart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_product = models.IntegerField(default=1)



class History(models.Model):
    id_history = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_product = models.IntegerField(default=1)
    purchase_date = models.DateField(default=datetime.now().date())

class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    name_customer = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()