import unittest
from store.serializers.contact_serializer import CreateContactSerializer


class TestCreateContactSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"receiver_username": "tester"}
        self.validated_data = {"receiver_username": "tester"}

    def test_create_contact_correct(self):
        serializer = CreateContactSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_contact_correct_delete_spaces(self):
        self.data["receiver_username"] = "   tester   "
        serializer = CreateContactSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_contact_correct_delete_spaces_max_length(self):
        self.data["receiver_username"] = "   " + "a" * 32 + "   "
        self.validated_data["receiver_username"] = "a" * 32
        serializer = CreateContactSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_contact_empty(self):
        self.data["receiver_username"] = ""
        serializer = CreateContactSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"receiver_username": "Username cannot be empty."})

    def test_create_contact_none(self):
        self.data["receiver_username"] = None
        serializer = CreateContactSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"receiver_username": "Username cannot be empty."})

    def test_create_contact_not_string(self):
        self.data["receiver_username"] = 2
        serializer = CreateContactSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"receiver_username": "Username must be a string."})

    def test_create_contact_too_long(self):
        self.data["receiver_username"] = "   " + "a" * 33 + "   "
        serializer = CreateContactSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"receiver_username": "Username cannot be longer than 32 characters."})
