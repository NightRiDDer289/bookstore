from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer

class ProductViewSet(ModelViewSet):
  serializer_class = ProductSerializer

  def get_queryset(self):
    return Product.objects.all().order_by('id')
  
class CategoryViewSet(ModelViewSet):
  serializer_class = CategorySerializer

  def get_queryset(self):
    return Category.objects.all().order_by('id')