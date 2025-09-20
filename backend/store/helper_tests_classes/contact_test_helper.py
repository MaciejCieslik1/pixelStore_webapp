from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.models import User, Contact


class ContactTestHelper:
    @staticmethod
    def create_contact(user: User) -> Contact:
        user2_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        AuthenticationHelper.register_and_login_user(user2_data)
        user2 = User.objects.get(username=user2_data["username"])
        contact = Contact(sender=user, receiver=user2)
        contact.save()
        return contact