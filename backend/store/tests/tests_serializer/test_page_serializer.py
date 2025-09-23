import unittest
from store.serializers.page_serializer import PageSerializer


class TestPageSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"page": 2, "page_size": 20}
        self.validated_data = {"page": 2, "page_size": 20}

    def test_find_all_success(self):
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_min_page_edge_case(self):
        self.data["page"] = 1
        self.validated_data["page"] = 1
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_min_page_size_edge_case(self):
        self.data["page_size"] = 1
        self.validated_data["page_size"] = 1
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_max_page_size_edge_case(self):
        self.data["page_size"] = 100
        self.validated_data["page_size"] = 100
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_empty_page(self):
        self.data["page"] = ""
        self.validated_data["page"] = 1
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_empty_page_size(self):
        self.data["page_size"] = ""
        self.validated_data["page_size"] = 10
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_invalid_data_page(self):
        self.data["page"] = "fwefefefe"
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page": "Page number must be a positive integer."})

    def test_find_all_invalid_data_page_size(self):
        self.data["page_size"] = "sffssffs"
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})

    def test_find_all_invalid_min_page(self):
        self.data["page"] = 0
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page": "Page number must be a positive integer."})

    def test_find_all_invalid_min_page_size(self):
        self.data["page_size"] = 0
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})

    def test_find_all_invalid_max_page_size(self):
        self.data["page_size"] = 101
        serializer = PageSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})
