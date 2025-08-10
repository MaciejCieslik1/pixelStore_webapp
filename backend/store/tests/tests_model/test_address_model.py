import unittest

from store.models import User, Address


class TestAddressModel(unittest.TestCase):
    def setUp(self):
        self.user = User(email="test@example.com", username="testuser", password="hashedpwd", is_verified=False,
            bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

    def test_eq_same_data(self):
        address1 = Address(user=self.user, address="aaaaaaa", postal_code="00001", city="Warsaw", country="Poland")
        address2 = Address(user=self.user, address="aaaaaaa", postal_code="00001", city="Warsaw", country="Poland")
        self.assertEqual(address1, address2)

    def test_eq_different_data(self):
        address1 = Address(user=self.user, address="aaaaaaa", postal_code="00001", city="Warsaw", country="Poland")
        address2 = Address(user=self.user, address="bbbbbbb", postal_code="00001", city="Warsaw", country="Poland")
        self.assertNotEquals(address1, address2)

    def test_hash_same_data(self):
        address1 = Address(user=self.user, address="aaaaaaa", postal_code="00001", city="Warsaw", country="Poland")
        address2 = Address(user=self.user, address="aaaaaaa", postal_code="00001", city="Warsaw", country="Poland")
        self.assertEqual(hash(address1), hash(address2))

    def test_hash_different_data(self):
        address1 = Address(user=self.user, address="aaaaaaa", postal_code="00001", city="Warsaw", country="Poland")
        address2 = Address(user=self.user, address="bbbbbbb", postal_code="00001", city="Warsaw", country="Poland")
        self.assertNotEquals(hash(address1), hash(address2))

    def test_create_address(self):
        data = {"address": "aaaaa", "postal_code": "12345", "city": "Warsaw", "country": "Poland"}

        address = Address.create_address(data, self.user)

        self.assertIsInstance(address, Address)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.address, data["address"])
        self.assertEqual(address.postal_code, data["postal_code"])
        self.assertEqual(address.city, data["city"])
        self.assertEqual(address.country, data["country"])


if __name__ == "__main__":
    unittest.main()
