from rest_framework import serializers
from .models import User, Product, History, Cart, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id_user","name_user", "email", "date_of_birth", "password", "phone_number", "position"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id_product","name_product", "img_product", "description", "price", "quantity"]

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ["id_history", "id_user", "id_product", "number_of_product"]

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id_cart", "id_user", "id_product", "number_of_product"]

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id_feedback", "name_customer", "email", "comment"]