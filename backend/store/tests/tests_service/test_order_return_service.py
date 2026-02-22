import datetime
from decimal import Decimal

import pytest
from django.utils import timezone

from store.exceptions import InvalidInputData, TokenExpiredError, IncorrectTokenError, TokenExpiredByReplacementError
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper, TokenTestsHelper
from store.helper_tests_classes.order_product_test_helper import OrderProductTestHelper
from store.helper_tests_classes.order_return_test_helper import OrderReturnTestHelper
from store.models import User, OrderReturn, Notification
from store.service.order_return_service import FindByIdOrderReturnService, CreateOrderReturnService, \
    UpdateOrderReturnService


@pytest.mark.django_db
class TestFindByIdOrderReturnService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.order_return = OrderReturnTestHelper.create_order_return(self.user)
        self.order_return_data = {"order_return_id": self.order_return.order_return_id,
            "order_product_id": self.order_return.order_product.order_product_id, "description": self.order_return.description,
            "return_date_time": self.order_return.return_date_time.isoformat().replace("+00:00", "Z"), "is_accepted": self.order_return.is_accepted}
        self.service = FindByIdOrderReturnService()

    def test_find_by_id(self):
        order_return_id = self.order_return.order_return_id
        order_returns_before = OrderReturn.objects.count()

        result = self.service.find_by_id(self.token, self.user, order_return_id)
        order_returns_after = OrderReturn.objects.count()

        assert result == self.order_return_data
        assert order_returns_before == order_returns_after

    def test_find_by_id_invalid_id(self):
        order_return_id = self.order_return.order_return_id + 1
        order_returns_before = OrderReturn.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token, self.user, order_return_id)
        order_returns_after = OrderReturn.objects.count()

        assert "Order return with provided id does not exist." in str(e.value)
        assert order_returns_before == order_returns_after

    def test_find_by_id_user_is_not_owner_of_transaction_but_seller(self):
        seller2_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                             "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                             "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                             "country": "Poland"}
        token_seller2 = AuthenticationHelper.register_and_login_user(seller2_data)
        seller2 = User.objects.get(username=seller2_data["username"])
        order_product = self.order_return.order_product
        order_product.seller = seller2
        order_product.save()
        order_return_id = self.order_return.order_return_id
        order_returns_before = OrderReturn.objects.count()

        result = self.service.find_by_id(token_seller2, seller2, order_return_id)
        order_returns_after = OrderReturn.objects.count()

        assert result == self.order_return_data
        assert order_returns_before == order_returns_after

    def test_find_by_id_user_is_neither_owner_of_transaction_nor_seller(self):
        self.seller3_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        self.token_seller3 = AuthenticationHelper.register_and_login_user(self.seller3_data)
        self.seller3 = User.objects.get(username=self.seller3_data["username"])
        order_return_id = self.order_return.order_return_id
        order_returns_before = OrderReturn.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token_seller3, self.seller3, order_return_id)
        order_returns_after = OrderReturn.objects.count()

        assert "Transaction in which order exists does not belong to the user." in str(e.value)
        assert order_returns_before == order_returns_after



    def test_find_by_id_expired_access_token(self):
        order_return_id = self.order_return.order_return_id
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        order_returns_before = OrderReturn.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find_by_id(access_token, self.user, order_return_id)
        order_returns_after = OrderReturn.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert order_returns_before == order_returns_after

    def test_find_by_id_incorrect_access_token(self):
        order_return_id = self.order_return.order_return_id + 1
        access_token = "invalid token"
        order_returns_before = OrderReturn.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.find_by_id(access_token, self.user, order_return_id)
        order_returns_after = OrderReturn.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert order_returns_before == order_returns_after

    def test_find_by_id_expired_by_replacement_access_token(self):
        order_return_id = self.order_return.order_product_id + 1
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        self.user = User.objects.get(username="tester")
        order_returns_before = OrderReturn.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find_by_id(access_token_first, self.user, order_return_id)
        order_returns_after = OrderReturn.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert order_returns_before == order_returns_after


@pytest.mark.django_db
class TestCreateOrderReturnService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.order_product = OrderProductTestHelper.create_order_products(self.user)
        self.order_return_creation_data = {"order_product_id": self.order_product.order_product_id,
                                  "description": "example_description"}
        self.created_communicate = "Order return created successfully."
        self.service = CreateOrderReturnService()

    def create(self):
        order_returns_before = OrderReturn.objects.count()
        notifications_count_before = Notification.objects.count()

        result = self.service.create(self.token, self.user, self.order_return_creation_data)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert self.created_communicate == result
        assert order_returns_before == order_returns_after - 1
        assert notifications_count_before == notifications_count_after - 1

    def create_invalid_order_product_id(self):
        self.order_return_creation_data["order_product_id"] = self.order_product.order_product_id + 1
        order_returns_before = OrderReturn.objects.count()
        notifications_count_before = Notification.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_return_creation_data)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert "Order with provided id does not exist." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def create_invalid_order_user_is_not_owner_of_transaction(self):
        self.seller_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        self.token_seller = AuthenticationHelper.register_and_login_user(self.seller_data)
        self.seller = User.objects.get(username=self.seller_data["username"])
        order_returns_before = OrderReturn.objects.count()
        notifications_count_before = Notification.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token_seller, self.seller, self.order_return_creation_data)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert "Transaction in which order exists does not belong to the user." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def test_create_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        order_returns_before = OrderReturn.objects.count()
        notifications_count_before = Notification.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.create(access_token, self.user, self.order_return_creation_data)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def test_create_incorrect_access_token(self):
        access_token = "invalid token"
        order_returns_before = OrderReturn.objects.count()
        notifications_count_before = Notification.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.create(access_token, self.user, self.order_return_creation_data)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def test_create_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        self.user = User.objects.get(username="tester")
        order_returns_before = OrderReturn.objects.count()
        notifications_count_before = Notification.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.create(access_token_first, self.user, self.order_return_creation_data)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after


@pytest.mark.django_db
class TestUpdateOrderReturnService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.order_return = OrderReturnTestHelper.create_order_return(self.user)
        self.order_return_id = self.order_return.order_return_id
        self.updated_communicate = "Order return updated successfully."
        self.service = UpdateOrderReturnService()
        self.seller2_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 10000.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        self.token_seller2 = AuthenticationHelper.register_and_login_user(self.seller2_data)
        self.seller2 = User.objects.get(username=self.seller2_data["username"])
        self.seller2.money = Decimal(10000.00)
        self.seller2.save()
        order_product = self.order_return.order_product
        order_product.seller = self.seller2
        order_product.save()

    def test_update(self):
        order_returns_before = OrderReturn.objects.count()

        notifications_count_before = Notification.objects.count()
        result = self.service.update(self.token_seller2, self.seller2, self.order_return_id)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert result == self.updated_communicate
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after - 3

    def test_update_invalid_id(self):
        order_return_id = self.order_return_id + 1
        order_returns_before = OrderReturn.objects.count()

        notifications_count_before = Notification.objects.count()
        with pytest.raises(InvalidInputData) as e:
            self.service.update(self.token_seller2, self.seller2, order_return_id)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert "Order return with provided id does not exist." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def test_update_user_is_not_seller(self):
        order_return = OrderReturn.objects.get(order_return_id=self.order_return_id)
        order_return.order_product.seller = self.seller2
        order_return.save()
        order_returns_before = OrderReturn.objects.count()

        notifications_count_before = Notification.objects.count()
        with pytest.raises(InvalidInputData) as e:
            self.service.update(self.token, self.user, self.order_return_id)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert "User is not seller of the product." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def test_update_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        order_returns_before = OrderReturn.objects.count()

        notifications_count_before = Notification.objects.count()
        with pytest.raises(TokenExpiredError) as e:
            self.service.update(access_token, self.user, self.order_return_id)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def test_update_incorrect_access_token(self):
        access_token = "invalid token"
        order_returns_before = OrderReturn.objects.count()

        notifications_count_before = Notification.objects.count()
        with pytest.raises(IncorrectTokenError) as e:
            self.service.update(access_token, self.user, self.order_return_id)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after

    def test_update_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        self.user = User.objects.get(username="tester")
        order_returns_before = OrderReturn.objects.count()

        notifications_count_before = Notification.objects.count()
        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.update(access_token_first, self.user, self.order_return_id)
        order_returns_after = OrderReturn.objects.count()
        notifications_count_after = Notification.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert order_returns_before == order_returns_after
        assert notifications_count_before == notifications_count_after
