from django.test import TestCase

from order.factories import OrderFactory, UserFactory
from order.serializers import OrderSerializer
from product.factories import CategoryFactory, ProductFactory

class OrderSerializerTest(TestCase):

  def setUp(self):
    self.category = CategoryFactory()
    self.product_1 = ProductFactory(category=[self.category])
    self.product_1.price = 100
    self.product_1.save()
    self.product_2 = ProductFactory(category=[self.category])
    self.product_2.price = 50
    self.product_2.save()
    self.user = UserFactory()
    self.order = OrderFactory(
        user=self.user,
        product=[self.product_1, self.product_2],
    )

  def test_serializer_fields(self):
    serializer = OrderSerializer(self.order)
    self.assertEqual(
      set(serializer.data.keys()),
      {'product', 'total'},
    )

  def test_serializer_total_is_sum_of_product_prices(self):
    serializer = OrderSerializer(self.order)
    expected_total = self.product_1.price + self.product_2.price
    self.assertEqual(serializer.data['total'], expected_total)

  def test_serializer_total_with_single_product(self):
    user = UserFactory()
    order = OrderFactory(user=user, product=[self.product_1])
    serializer = OrderSerializer(order)
    self.assertEqual(serializer.data['total'], self.product_1.price)

  def test_serializer_contains_nested_products(self):
    serializer = OrderSerializer(self.order)
    self.assertIsInstance(serializer.data['product'], list)
    self.assertEqual(len(serializer.data['product']), 2)

  def test_serializer_nested_product_fields(self):
    serializer = OrderSerializer(self.order)
    product_data = serializer.data['product'][0]
    self.assertEqual(
      set(product_data.keys()),
      {'title', 'description', 'price', 'active', 'category'},
    )

  def test_serializer_nested_product_contains_category(self):
    serializer = OrderSerializer(self.order)
    for product_data in serializer.data['product']:
      self.assertIsInstance(product_data['category'], list)
      self.assertGreater(len(product_data['category']), 0)
