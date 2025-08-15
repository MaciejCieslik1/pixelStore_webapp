import unittest
from store.models import User, UserPreferences


class TestUserPreferencesModel(unittest.TestCase):
    def setUp(self):
        self.user = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

    def test_eq_same_data(self):
        user_preferences1 = UserPreferences(user=self.user, dark_mode=True)
        user_preferences2 = UserPreferences(user=self.user, dark_mode=True)

        self.assertEqual(user_preferences1, user_preferences2)

    def test_eq_different_data(self):
        user_preferences1 = UserPreferences(user=self.user, dark_mode=True)
        user_preferences2 = UserPreferences(user=self.user, dark_mode=False)

        self.assertNotEqual(user_preferences1, user_preferences2)

    def test_hash_same_data(self):
        user_preferences1 = UserPreferences(user=self.user, dark_mode=True)
        user_preferences2 = UserPreferences(user=self.user, dark_mode=True)

        self.assertEqual(hash(user_preferences1), hash(user_preferences2))

    def test_hash_different_data(self):
        user_preferences1 = UserPreferences(user=self.user, dark_mode=True)
        user_preferences2 = UserPreferences(user=self.user, dark_mode=False)

        self.assertNotEqual(hash(user_preferences1), hash(user_preferences2))

    def test_create_user_preferences(self):
        user_preferences = UserPreferences.create_user_preferences(self.user)

        self.assertIsInstance(user_preferences, UserPreferences)
        self.assertEqual(user_preferences.user, self.user)
        self.assertEqual(user_preferences.dark_mode, False)

