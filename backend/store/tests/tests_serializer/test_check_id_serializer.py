import unittest

from store.serializers.check_id_serializer import CheckIdSerializer


class TestCheckSerializer(unittest.TestCase):
    def test_check_id_success(self):
        order_product_id = 1
        serializer = CheckIdSerializer(id=order_product_id, name="Order product")

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.error, None)

    def test_check_id_empty_id(self):
        order_product_id = None
        serializer = CheckIdSerializer(id=order_product_id, name="Order product")

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id cannot be empty.")

    def test_check_id_string(self):
        order_product_id = "sfdfffs"
        serializer = CheckIdSerializer(id=order_product_id, name="Order product")

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id must be positive integer.")

    def test_check_id_not_positive_integer(self):
        order_product_id = 0
        serializer = CheckIdSerializer(id=order_product_id, name="Order product")

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id must be positive integer.")

