from django.utils.text import slugify
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
    extra_kwargs = {'slug': {'required': False}}

  def create(self, validated_data):
    if 'slug' not in validated_data:
      validated_data['slug'] = slugify(validated_data['title'])
    return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
  category = CategorySerializer(read_only=True, many=True)
  categories_id = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    write_only=True,
    many=True
  )

  class Meta:
    model = Product
    fields = [
      'title',
      'description',
      'price',
      'active',
      'category',
      'categories_id',
    ]

  def create(self, validated_data):
    category_data = validated_data.pop('categories_id')

    product = Product.objects.create(**validated_data)
    for category in category_data:
      product.category.add(category)

    return product