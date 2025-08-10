import unittest

from store.models import User, Contact


class TestContactModel(unittest.TestCase):
    def setUp(self):
        self.sender1 = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
             bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.sender2 = User(email="sender@example.com", username="testuser2", password="hashedpwd", is_verified=False,
                            bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.receiver1 = User(email="receiver@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                       bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.receiver2 = User(email="receiver@example.com", username="testuser2", password="hashedpwd", is_verified=False,
                              bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

    def test_eq_same_data(self):
        contact1 = Contact(sender=self.sender1, receiver=self.receiver1)
        contact2 = Contact(sender=self.sender1, receiver=self.receiver1)

        self.assertEqual(contact1, contact2)

    def test_eq_different_data(self):
        contact1 = Contact(sender=self.sender1, receiver=self.receiver1)
        contact2 = Contact(sender=self.sender2, receiver=self.receiver1)

        self.assertNotEquals(contact1, contact2)

    def test_hash_same_data(self):
        contact1 = Contact(sender=self.sender1, receiver=self.receiver1)
        contact2 = Contact(sender=self.sender1, receiver=self.receiver1)

        self.assertEqual(hash(contact1), hash(contact2))

    def test_hash_different_data(self):
        contact1 = Contact(sender=self.sender1, receiver=self.receiver1)
        contact2 = Contact(sender=self.sender1, receiver=self.receiver2)

        self.assertNotEquals(hash(contact1), hash(contact2))


if __name__ == "__main__":
    unittest.main()
