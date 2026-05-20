from rest_framework import serializers

from product.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = [
      'title',
      'slug',
      'description',
      'active',
    ]

class ProductSerializer(serializers.ModelSerializer):
  category = CategorySerializer(required=True, many=True)

  class Meta:
    model = Product
    fields = [
      'title',
      'description',
      'price',
      'active',
      'category',
    ]