import unittest

from store.serializers.product_serializer import CreateProductSerializer, FindAllProductsSerializer


class TestFindAllProductsSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"owner_username": "tester", "name": "example_name", "min_price": 100, "max_price": 10000,
            "status": "available", "ordering_field": "price", "order": "asc", "page": 2, "page_size": 20}
        self.validated_data = {"owner_username": "tester", "name": "example_name", "min_price": 100, "max_price": 10000,
                     "status": "available", "ordering_field": "price", "order": "asc", "page": 2, "page_size": 20}

    def test_find_all_success(self):
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_order_desc(self):
        self.data["order"] = "desc"
        self.validated_data["order"] = "desc"
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_success_delete_spaces(self):
        self.data = {"owner_username": "  tester  ", "name": "  example_name  ", "min_price": 100, "max_price": 10000,
                     "status": "  available  ", "ordering_field": " price ", "order": "  asc  ", "page": 2, "page_size": 20}
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_min_price_min_integer(self):
        self.data["max_price"] = 1
        self.validated_data["max_price"] = 1
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_min_page_edge_case(self):
        self.data["page"] = 1
        self.validated_data["page"] = 1
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_min_page_size_edge_case(self):
        self.data["page_size"] = 1
        self.validated_data["page_size"] = 1
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_max_page_size_edge_case(self):
        self.data["page_size"] = 100
        self.validated_data["page_size"] = 100
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_bad_status(self):
        self.data["status"] = "bad_status"
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"status": "Status must be one of following: 'available', 'unavailable', 'archived'."})

    def test_find_all_bad_order(self):
        self.data["order"] = "fefeef"
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"order": "Order must be: 'asc' or 'desc'."})

    def test_find_all_bad_ordering_field(self):
        self.data["ordering_field"] = "fefeef"
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"ordering_field": "Ordering field must be one of following: 'name', 'price', 'status'."})

    def test_find_all_invalid_data_page(self):
        self.data["page"] = "fwefefefe"
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page": "Page number must be a positive integer."})

    def test_find_all_invalid_data_page_size(self):
        self.data["page_size"] = "sffssffs"
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})

    def test_find_all_invalid_min_page(self):
        self.data["page"] = 0
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page": "Page number must be a positive integer."})

    def test_find_all_invalid_min_page_size(self):
        self.data["page_size"] = 0
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})

    def test_find_all_invalid_max_page_size(self):
        self.data["page_size"] = 101
        serializer = FindAllProductsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})

    def test_find_all_empty_username(self):
        self.data["owner_username"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"owner_username": "Username cannot be empty."})

    def test_find_all_none_username(self):
        self.data["owner_username"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"owner_username": "Username cannot be empty."})

    def test_find_all_not_string_username(self):
        self.data["owner_username"] = 9
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"owner_username": "Username must be a string."})

    def test_find_all_empty_name(self):
        self.data["name"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Product name cannot be empty."})

    def test_find_all_none_name(self):
        self.data["name"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Product name cannot be empty."})

    def test_find_all_not_string_name(self):
        self.data["name"] = 9
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Product name must be a string."})

class TestCreateProductSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"owner_username": "tester", "name": "example_name", "description": "example_text", "price": 1000,
            "amount": 5, "color": "red", "weight": 5, "length": 3, "width": 3, "height": 3, "guarantee_period": 1,
            "status": "available"}
        self.validated_data = {"owner_username": "tester", "name": "example_name", "description": "example_text", "price": 1000,
             "amount": 5, "color": "red", "weight": 5, "length": 3, "width": 3, "height": 3, "guarantee_period": 1,
             "status": "available"}

    def test_create_success(self):
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_success_delete_spaces(self):
        self.data = {"owner_username": "  tester  ", "name": "  example_name  ", "description": "  example_text ", "price": 1000,
            "amount": 5, "color": "  red  ", "weight": 5, "length": 3, "width": 3, "height": 3,
            "guarantee_period": 1, "status": "  available  "}
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_price_max_integer(self):
        self.data["price"] = 999999
        self.validated_data["price"] = 999999
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_price_max_decimal(self):
        self.data["price"] = 999999.99
        self.validated_data["price"] = 999999.99
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_weight_max_integer(self):
        self.data["weight"] = 99
        self.validated_data["weight"] = 99
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_weight_max_decimal(self):
        self.data["weight"] = 99.99
        self.validated_data["weight"] =99.99
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_length_max_integer(self):
        self.data["length"] = 999
        self.validated_data["length"] = 999
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_length_max_decimal(self):
        self.data["length"] = 999.99
        self.validated_data["length"] =999.99
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_width_max_integer(self):
        self.data["width"] = 999
        self.validated_data["width"] = 999
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_width_max_decimal(self):
        self.data["width"] = 999.99
        self.validated_data["width"] =999.99
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_height_max_integer(self):
        self.data["height"] = 999
        self.validated_data["height"] = 999
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_height_max_decimal(self):
        self.data["height"] = 999.99
        self.validated_data["height"] = 999.99
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_status_unavailable(self):
        self.data["status"] = "unavailable"
        self.validated_data["status"] = "unavailable"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_status_archived(self):
        self.data["status"] = "archived"
        self.validated_data["status"] = "archived"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_empty_username(self):
        self.data["owner_username"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"owner_username": "Username cannot be empty."})

    def test_create_none_username(self):
        self.data["owner_username"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"owner_username": "Username cannot be empty."})

    def test_create_not_string_username(self):
        self.data["owner_username"] = 9
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"owner_username": "Username must be a string."})

    def test_create_empty_name(self):
        self.data["name"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Product name cannot be empty."})

    def test_create_none_name(self):
        self.data["name"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Product name cannot be empty."})

    def test_create_not_string_name(self):
        self.data["name"] = 9
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Product name must be a string."})

    def test_create_empty_description(self):
        self.data["description"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description cannot be empty."})

    def test_create_none_description(self):
        self.data["description"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description cannot be empty."})

    def test_create_not_string_description(self):
        self.data["description"] = 9
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description must be string."})

    def test_create_none_price(self):
        self.data["price"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"price": "Price cannot be empty."})

    def test_create_not_number_price(self):
        self.data["price"] = "fffe"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"price": "Price must be positive integer or decimal."})

    def test_create_none_amount(self):
        self.data["amount"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"amount": "Amount cannot be empty."})

    def test_create_not_number_amount(self):
        self.data["amount"] = "fffe"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"amount": "Amount must be positive integer."})

    def test_create_empty_color(self):
        self.data["color"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"color": "Color cannot be empty."})

    def test_create_none_color(self):
        self.data["color"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"color": "Color cannot be empty."})

    def test_create_not_string_color(self):
        self.data["color"] = 2
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"color": "Color must be string."})

    def test_create_empty_weight(self):
        self.data["weight"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"weight": "Weight must be positive integer or decimal."})

    def test_create_none_weight(self):
        self.data["weight"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"weight": "Weight cannot be empty."})

    def test_create_not_int_weight(self):
        self.data["weight"] = "cffefefe"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"weight": "Weight must be positive integer or decimal."})

    def test_create_empty_length(self):
        self.data["length"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"length": "Length must be positive integer or decimal."})

    def test_create_none_length(self):
        self.data["length"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"length": "Length cannot be empty."})

    def test_create_not_int_length(self):
        self.data["length"] = "cffefefe"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"length": "Length must be positive integer or decimal."})

    def test_create_none_height(self):
        self.data["height"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"height": "Height cannot be empty."})

    def test_create_not_int_height(self):
        self.data["height"] = "cffefefe"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"height": "Height must be positive integer or decimal."})

    def test_create_empty_width(self):
        self.data["width"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"width": "Width must be positive integer or decimal."})

    def test_create_none_width(self):
        self.data["width"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"width": "Width cannot be empty."})

    def test_create_not_int_width(self):
        self.data["width"] = "cffefefe"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"width": "Width must be positive integer or decimal."})

    def test_create_none_guarantee_period(self):
        self.data["guarantee_period"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"guarantee_period": "Guarantee period cannot be empty."})

    def test_create_not_int_guarantee_period(self):
        self.data["guarantee_period"] = "cffefefe"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"guarantee_period": "Guarantee period must be positive integer."})

    def test_create_empty_status(self):
        self.data["status"] = ""
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"status": "Status must be one of following: 'available', 'unavailable', 'archived'."})

    def test_create_none_status(self):
        self.data["status"] = None
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"status": "Status must be one of following: 'available', 'unavailable', 'archived'."})

    def test_create_not_enum_status(self):
        self.data["status"] = "rgeegergerre"
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"status": "Status must be one of following: 'available', 'unavailable', 'archived'."})

    def test_create_price_not_positive_integer(self):
        self.data["price"] = 0
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"price": "Price must be positive integer or decimal."})

    def test_create_price_too_big_integer(self):
        self.data["price"] = 1000000
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"price": "Price must be less than 1000000.00."})

    def test_create_price_too_big_decimal(self):
        self.data["price"] = 1000000.00
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"price": "Price must be less than 1000000.00."})

    def test_create_amount_negative_integer(self):
        self.data["amount"] = -1
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"amount": "Amount must be positive integer."})

    def test_create_weight_not_positive_integer(self):
        self.data["weight"] = 0
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"weight": "Weight must be positive integer or decimal."})

    def test_create_weight_too_big_integer(self):
        self.data["weight"] = 100
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"weight": "Weight must be less than 100.00."})

    def test_create_weight_too_big_decimal(self):
        self.data["weight"] = 100.00
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"weight": "Weight must be less than 100.00."})

    def test_create_length_not_positive_integer(self):
        self.data["length"] = 0
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"length": "Length must be positive integer or decimal."})

    def test_create_length_too_big_integer(self):
        self.data["length"] = 1000
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"length": "Length must be less than 1000.00."})

    def test_create_length_too_big_decimal(self):
        self.data["length"] = 1000.00
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"length": "Length must be less than 1000.00."})

    def test_create_width_not_positive_integer(self):
        self.data["width"] = 0
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"width": "Width must be positive integer or decimal."})

    def test_create_width_too_big_integer(self):
        self.data["width"] = 1000
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"width": "Width must be less than 1000.00."})

    def test_create_width_too_big_decimal(self):
        self.data["width"] = 1000.00
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"width": "Width must be less than 1000.00."})

    def test_create_height_not_positive_integer(self):
        self.data["height"] = 0
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"height": "Height must be positive integer or decimal."})

    def test_create_height_too_big_integer(self):
        self.data["height"] = 1000
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"height": "Height must be less than 1000.00."})

    def test_create_height_too_big_decimal(self):
        self.data["height"] = 1000.00
        serializer = CreateProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"height": "Height must be less than 1000.00."})


