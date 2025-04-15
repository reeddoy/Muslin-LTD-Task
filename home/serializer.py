from rest_framework import serializers
from home.models import Product_Category, Product, Product_Image, Available_Stock
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Image
        fields = ['id', 'image']

class AvailableStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Available_Stock
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()    
    class Meta:
        model = Product
        exclude = ['original_price']
