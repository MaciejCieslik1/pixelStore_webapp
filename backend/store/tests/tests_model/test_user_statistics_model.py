import unittest
from datetime import datetime, date

from store.models import User, UserStatistics


class TestUserStatisticsModel(unittest.TestCase):
    def setUp(self):
        self.user = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

    def test_eq_same_data(self):
        user_statistics1 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                           products_sold=0)
        user_statistics2 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                          products_sold=0)

        self.assertEqual(user_statistics1, user_statistics2)

    def test_eq_different_data(self):
        user_statistics1 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                          products_sold=0)
        user_statistics2 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                          products_sold=1)

        self.assertNotEqual(user_statistics1, user_statistics2)

    def test_hash_same_data(self):
        user_statistics1 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                          products_sold=0)
        user_statistics2 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                          products_sold=0)

        self.assertEqual(hash(user_statistics1), hash(user_statistics2))

    def test_hash_different_data(self):
        user_statistics1 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                          products_sold=0)
        user_statistics2 = UserStatistics(user=self.user, creation_date=date.today(), products_bought=0,
                                          products_sold=1)

        self.assertNotEqual(hash(user_statistics1), hash(user_statistics2))

    def test_create_user_statistics(self):
        user_statistics = UserStatistics.create_user_statistics(self.user)

        self.assertIsInstance(user_statistics, UserStatistics)
        self.assertEqual(user_statistics.user, self.user)
        self.assertEqual(user_statistics.creation_date, date.today())
        self.assertEqual(user_statistics.products_bought, 0)
        self.assertEqual(user_statistics.products_sold, 0)
