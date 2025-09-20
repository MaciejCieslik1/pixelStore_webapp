import unittest

from store.serializers.order_return_serializer import CreateOrderReturnSerializer


class TestCreateOrderProductSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"order_product_id": 1, "description": "description"}
        self.validated_data = {"order_product_id": 1, "description": "description"}

    def test_create_success(self):
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_success_delete_spaces(self):
        self.data["description"] = "  description   "
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_order_description_max_length(self):
        self.data["description"] = 1024 * "a"
        self.validated_data["description"] = 1024 * "a"
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_order_description_max_length_spaces(self):
        self.data["description"] = "   " + 1024 * "a" + "  "
        self.validated_data["description"] = 1024 * "a"
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_empty_order_product_id(self):
        self.data["order_product_id"] = None
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"order_product_id": "Order product id cannot be empty."})

    def test_create_order_product_id_string(self):
        self.data["order_product_id"] = "sfdfffs"
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"order_product_id": "Order product id must be positive integer."})

    def test_create_product_id_not_positive_integer(self):
        self.data["order_product_id"] = 0
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"order_product_id": "Order product id must be positive integer."})

    def test_create_empty_description(self):
        self.data["description"] = None
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description cannot be empty."})

    def test_create_order_description_not_string(self):
        self.data["description"] = 123
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description must be string."})

    def test_create_order_description_too_long(self):
        self.data["description"] = 1025 * "a"
        serializer = CreateOrderReturnSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description must be less than 1025 characters."})
