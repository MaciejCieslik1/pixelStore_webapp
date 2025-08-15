import unittest
from datetime import datetime

from store.models import User, Transaction


class TestProductReviewModel(unittest.TestCase):
    def setUp(self):
        self.buyer = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                          bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.now = datetime.now()

    def test_eq_same_data(self):
        transaction1 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=False)
        transaction2 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=False)

        self.assertEqual(transaction1, transaction2)

    def test_eq_different_data(self):
        transaction1 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=False)
        transaction2 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=True)

        self.assertNotEqual(transaction1, transaction2)

    def test_hash_same_data(self):
        now = datetime.now()
        transaction1 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=False)
        transaction2 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=False)

        self.assertEqual(hash(transaction1), hash(transaction2))

    def test_hash_different_data(self):
        transaction1 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=False)
        transaction2 = Transaction(buyer=self.buyer, total_price=1000, date_time=self.now, is_finished=True)

        self.assertNotEqual(hash(transaction1), hash(transaction2))
