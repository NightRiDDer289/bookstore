from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers import CategorySerializer, ProductSerializer

class CategorySerializerTest(TestCase):

  def setUp(self):
    self.category = CategoryFactory()

  def test_serializer_fields(self):
    serializer = CategorySerializer(self.category)
    self.assertEqual(
      set(serializer.data.keys()),
      {'title', 'slug', 'description', 'active'},
    )

  def test_serializer_with_valid_data(self):
    data = {
      'title': 'Fiction',
      'slug': 'fiction',
      'description': 'Fiction books',
      'active': True,
    }
    serializer = CategorySerializer(data=data)
    self.assertTrue(serializer.is_valid())

  def test_serializer_invalid_without_title(self):
    data = {'slug': 'fiction'}
    serializer = CategorySerializer(data=data)
    self.assertFalse(serializer.is_valid())
    self.assertIn('title', serializer.errors)

  def test_serializer_invalid_without_slug(self):
    data = {'title': 'Fiction'}
    serializer = CategorySerializer(data=data)
    self.assertFalse(serializer.is_valid())
    self.assertIn('slug', serializer.errors)

  def test_serializer_data_matches_model(self):
    serializer = CategorySerializer(self.category)
    self.assertEqual(serializer.data['title'], self.category.title)
    self.assertEqual(serializer.data['slug'], self.category.slug)
    self.assertEqual(serializer.data['active'], self.category.active)


class ProductSerializerTest(TestCase):
  def setUp(self):
    self.category = CategoryFactory()
    self.product = ProductFactory(category=[self.category])

  def test_serializer_fields(self):
    serializer = ProductSerializer(self.product)
    self.assertEqual(
      set(serializer.data.keys()),
      {'title', 'description', 'price', 'active', 'category'},
    )

  def test_serializer_contains_nested_category(self):
    serializer = ProductSerializer(self.product)
    self.assertIsInstance(serializer.data['category'], list)
    self.assertEqual(len(serializer.data['category']), 1)
    self.assertEqual(
      serializer.data['category'][0]['title'],
      self.category.title,
    )

  def test_serializer_data_matches_model(self):
    serializer = ProductSerializer(self.product)
    self.assertEqual(serializer.data['title'], self.product.title)
    self.assertEqual(serializer.data['price'], self.product.price)
    self.assertEqual(serializer.data['active'], self.product.active)

  def test_serializer_with_multiple_categories(self):
    extra_category = CategoryFactory()
    self.product.category.add(extra_category)
    serializer = ProductSerializer(self.product)
    self.assertEqual(len(serializer.data['category']), 2)
