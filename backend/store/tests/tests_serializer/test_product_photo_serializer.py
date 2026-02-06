import unittest

from store.serializers.product_photo_serializer import CreateProductPhotoSerializer


class TestCreateProductPhotoSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"product_id": 1, "image_url": "example_url", "is_main_photo": True}
        self.validated_data = {"product_id": 1, "image_url": "example_url", "is_main_photo": True}

    def test_create_success(self):
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_success_delete_spaces(self):
        self.data = {"product_id": 1, "image_url": "   example_url   ", "is_main_photo": True}
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_none_product_id(self):
        self.data["product_id"] = None
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"product_id": "Product id cannot be empty."})

    def test_create_product_id_not_int(self):
        self.data["product_id"] = "1"
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"product_id": "Product id must be positive integer."})

    def test_create_none_image_url(self):
        self.data["image_url"] = None
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"image_url": "Image url cannot be empty."})

    def test_create_empty_image_url(self):
        self.data["image_url"] = ""
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"image_url": "Image url cannot be empty."})

    def test_create_image_url_not_string(self):
        self.data["image_url"] = 12
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"image_url": "Image url must be a string."})

    def test_create_none_is_main_photo(self):
        self.data["is_main_photo"] = None
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"is_main_photo": "Is main photo flag cannot be empty."})


    def test_create_is_main_photo_not_bool(self):
        self.data["is_main_photo"] = 12
        serializer = CreateProductPhotoSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"is_main_photo": "Is main photo flag must be bool."})
