import unittest

from store.serializers.update_user_preferences_serializer import UpdateUserPreferencesSerializer


class TestUpdateUserSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"dark_mode": True}
        self.validated_data = {"dark_mode": True}

    def test_update_success(self):
        serializer = UpdateUserPreferencesSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_none_dark_mode(self):
        self.data["dark_mode"] = None
        self.validated_data["dark_mode"] = False
        serializer = UpdateUserPreferencesSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_invalid_dark_mode_type(self):
        self.data["dark_mode"] = 12
        serializer = UpdateUserPreferencesSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"dark_mode": "Dark mode must be bool."})
