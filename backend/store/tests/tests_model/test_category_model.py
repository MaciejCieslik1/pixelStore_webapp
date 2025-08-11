import unittest

from store.models import Category


class TestCategory(unittest.TestCase):
    def test_eq_same_data(self):
        category1 = Category(name="aaaa", description="bbbb")
        category2 = Category(name="aaaa", description="bbbb")

        self.assertEqual(category1, category2)

    def test_eq_different_data(self):
        category1 = Category(name="aaaa", description="bbbb")
        category2 = Category(name="ccc", description="bbbb")

        self.assertNotEqual(category1, category2)

    def test_hash_same_data(self):
        category1 = Category(name="aaaa", description="bbbb")
        category2 = Category(name="aaaa", description="bbbb")

        self.assertEqual(hash(category1), hash(category2))

    def test_hash_different_data(self):
        category1 = Category(name="aaaa", description="bbbb")
        category2 = Category(name="ccc", description="bbbb")

        self.assertNotEqual(hash(category1), hash(category2))
