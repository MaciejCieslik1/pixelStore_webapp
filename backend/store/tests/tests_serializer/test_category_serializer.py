import unittest
from store.serializers.category_serializer import FindCategoryByNameSerializer, CreateCategorySerializer


class TestFindCategoryByNameSerializer(unittest.TestCase):
    def setUp(self):
        self.name = "example_name1"
        self.validated_name = "example_name1"

    def test_find_category_by_name_success(self):
        serializer = FindCategoryByNameSerializer(name=self.name)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_name, self.validated_name)
        self.assertEqual(serializer.error, None)

    def test_find_category_by_name_success_delete_spaces(self):
        self.name = "   example_name1   "
        serializer = FindCategoryByNameSerializer(name=self.name)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_name, self.validated_name)
        self.assertEqual(serializer.error, None)

    def test_find_category_by_name_correct_data_max_name_edge_case(self):
        self.name = "example_name11111111111111111111"
        self.validated_name = "example_name11111111111111111111"
        serializer = FindCategoryByNameSerializer(name=self.name)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_name, self.validated_name)
        self.assertEqual(serializer.error, None)

    def test_find_category_by_name_empty_name(self):
        self.name = ""
        serializer = FindCategoryByNameSerializer(name=self.name)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_name, self.validated_name)
        self.assertEqual(serializer.error, "Category name is not provided.")

    def test_find_category_by_name_none_name(self):
        self.name = ""
        serializer = FindCategoryByNameSerializer(name=self.name)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_name, self.validated_name)
        self.assertEqual(serializer.error, "Category name is not provided.")

    def test_find_category_by_name_incorrect_too_long(self):
        self.name = "example_name111111111111111111111"
        serializer = FindCategoryByNameSerializer(name=self.name)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_name, self.validated_name)
        self.assertEqual(serializer.error, "Category name cannot be longer than 32 characters.")


class TestCreateCategorySerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"name": "example_name1", "description": "example_description1"}
        self.validated_data = {"name": "example_name1", "description": "example_description1"}

    def test_create_category_success(self):
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_category_success_delete_spaces(self):
        self.data["name"] = "   example_name1   "
        self.data["description"] = "   example_description1   "
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_category_correct_data_max_name_edge_case(self):
        self.data["name"] = "example_name11111111111111111111"
        self.validated_data["name"] = "example_name11111111111111111111"
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_category_correct_data_max_description_edge_case(self):
        self.data["description"] = "a" * 1024
        self.validated_data["description"] = "a" * 1024
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_category_empty_name(self):
        self.data["name"] = ""
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Category name is not provided."})

    def test_create_category_none_name(self):
        self.data["name"] = None
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Category name is not provided."})

    def test_create_category_empty_description(self):
        self.data["description"] = ""
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description is not provided."})

    def test_create_category_none_description(self):
        self.data["description"] = None
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description is not provided."})

    def test_create_category_incorrect_too_long_name(self):
        self.data["name"] = "a" * 33
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"name": "Category name cannot be longer than 32 characters."})

    def test_create_category_incorrect_too_long_description(self):
        self.data["description"] = "a" * 1025
        serializer = CreateCategorySerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description cannot be longer than 1024 characters."})
