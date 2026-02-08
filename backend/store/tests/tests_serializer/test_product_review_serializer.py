import unittest

from store.serializers.product_review_serializer import FindAllProductReviewsSerializer, \
    FindAllFromUserProductReviewsSerializer, CreateProductReviewSerializer


class TestFindAllProductReviewsSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"product_id": 1, "page": 2, "page_size": 20}
        self.validated_data = {"product_id": 1, "page": 2, "page_size": 20}


    def test_find_all_success(self):
        serializer = FindAllProductReviewsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


class TestFindAllFromUserProductReviewsSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"username": "tester", "page": 2, "page_size": 20}
        self.validated_data = {"username": "tester", "page": 2, "page_size": 20}


    def test_find_all_from_user_success(self):
        serializer = FindAllFromUserProductReviewsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


class TestCreateProductReviewSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"rating": 1.0, "description": "example"}
        self.validated_data = {"rating": 1, "description": "example"}

    def test_create_success(self):
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_success_delete_spaces(self):
        self.data = {"rating": 1.0, "description": "   example   "}
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_none_rating(self):
        self.data["rating"] = None
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"rating": "Rating cannot be empty."})

    def test_create_product_rating_not_double(self):
        self.data["rating"] = "1"
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"rating": "Rating must be decimal value from 1 to 5."})

    def test_create_product_rating_too_small(self):
        self.data["rating"] = 0.9
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"rating": "Rating must be decimal value from 1 to 5."})


    def test_create_product_rating_too_big(self):
        self.data["rating"] = 5.1
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"rating": "Rating must be decimal value from 1 to 5."})


    def test_create_none_description(self):
        self.data["description"] = None
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description cannot be empty."})


    def test_create_description_not_str(self):
        self.data["description"] = 12
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description must be text."})


    def test_create_description_too_long(self):
        self.data["description"] = "1" * 1025
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description length must be between 1 and 1024 characters."})


    def test_create_description_empty(self):
        self.data["description"] = ""
        serializer = CreateProductReviewSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"description": "Description length must be between 1 and 1024 characters."})
