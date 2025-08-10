import unittest
from store.models import User, Notification
from datetime import datetime


class TestNotificationModel(unittest.TestCase):
    def setUp(self):
        self.sender = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                            bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.receiver = User(email="sender@example.com", username="testuser2", password="hashedpwd", is_verified=False,
                            bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

    def test_eq_same_data(self):
        now = datetime.now()
        notification1 = Notification(sender=self.sender, receiver=self.receiver,
            sent_date_time=now, text="hello")
        notification2 = Notification(sender=self.sender, receiver=self.receiver,
            sent_date_time=now, text="hello")

        self.assertEqual(notification1, notification2)

    def test_eq_different_data(self):
        notification1 = Notification(sender=self.sender, receiver=self.receiver,
                                     sent_date_time=datetime.now(), text="hello")
        notification2 = Notification(sender=self.sender, receiver=self.receiver,
                                     sent_date_time=datetime.now(), text="bye")

        self.assertNotEquals(notification1, notification2)

    def test_hash_same_data(self):
        now = datetime.now()
        notification1 = Notification(sender=self.sender, receiver=self.receiver,
                                     sent_date_time=now, text="hello")
        notification2 = Notification(sender=self.sender, receiver=self.receiver,
                                     sent_date_time=now, text="hello")

        self.assertEqual(hash(notification1), hash(notification2))

    def test_hash_different_data(self):
        notification1 = Notification(sender=self.sender, receiver=self.receiver,
                                     sent_date_time=datetime.now(), text="hello")
        notification2 = Notification(sender=self.sender, receiver=self.receiver,
                                     sent_date_time=datetime.now(), text="bye")

        self.assertNotEquals(hash(notification1), hash(notification2))

if __name__ == "__main__":
    unittest.main()
