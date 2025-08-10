import unittest
from store.models import User


class TestUserModel(unittest.TestCase):
    def test_eq_same_data(self):
        user1 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                          bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        user2 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                          bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

        self.assertEqual(user1, user2)

    def test_eq_different_data(self):
        user1 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        user2 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=1)

        self.assertNotEquals(user1, user2)

    def test_hash_same_data(self):
        user1 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        user2 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

        self.assertEqual(hash(user1), hash(user2))

    def test_hash_different_data(self):
        user1 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        user2 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=1)

        self.assertNotEquals(hash(user1), hash(user2))
