import datetime

import pytest
from django.utils import timezone

from store.exceptions import InvalidInputData, TokenExpiredError, IncorrectTokenError, TokenExpiredByReplacementError
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper, TokenTestsHelper
from store.models import User, Transaction, Product, OrderProduct
from store.service.order_product_service import FindByIdOrderProductService, CreateOrderProductService, \
    UpdateOrderProductService, DeleteOrderProductService


@pytest.mark.django_db
class TestFindByIdOrderProductService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.seller_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        self.token_seller = AuthenticationHelper.register_and_login_user(self.seller_data)
        self.seller = User.objects.get(username=self.seller_data["username"])
        item_price = 1000
        transaction = Transaction(buyer=self.user, total_price=item_price, date_time=timezone.now(), is_finished=False)
        product = Product(owner=self.seller, name="fefeffe", description="fefeffe", amount=1, price=item_price, color="red",
            weihgt=2, length=3, width=3, height=3, guarantee_period=1, status="available")
        transaction.save()
        product.save()
        self.order_product = OrderProduct(product=product, transaction=transaction, seller=self.seller, shopping_price=item_price)
        self.order_product.save()
        self.service = FindByIdOrderProductService()
        self.order_product_data = {"order_product": 1, "transaction_id": 1, "product_id": 1, "seller_username": "tester2",
            "shopping_price": 1000}

    def test_find_by_id(self):
        order_product_id = 1
        order_products_before = OrderProduct.objects.count()

        result = self.service.find_by_id(self.token, self.user, order_product_id)
        order_products_after = OrderProduct.objects.count()

        assert self.order_product_data == result
        assert order_products_before == order_products_after

    def test_find_by_id_invalid_id(self):
        order_product_id = 2
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token, self.user, order_product_id)
        order_products_after = OrderProduct.objects.count()

        assert "Order with provided id does not exist." in str(e.value)
        assert order_products_before == order_products_after

    def test_find_by_id_user_is_not_owner_of_transaction(self):
        order_product_id = 1
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token_seller, self.seller, order_product_id)
        order_products_after = OrderProduct.objects.count()

        assert "Transaction in which order exists does not belong to the user." in str(e.value)
        assert order_products_before == order_products_after

    def test_find_by_id_expired_access_token(self):
        order_product_id = 1
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find_by_id(access_token, self.user, order_product_id)
        order_products_after = OrderProduct.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert order_products_before == order_products_after

    def test_find_by_id_incorrect_access_token(self):
        order_product_id = 1
        access_token = "invalid token"
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.find_by_id(access_token, self.user, order_product_id)
        order_products_after = OrderProduct.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert order_products_before == order_products_after

    def test_find_by_id_expired_by_replacement_access_token(self):
        order_product_id = 1
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find_by_id(access_token_first, self.user, order_product_id)
            order_products_after = OrderProduct.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert order_products_before == order_products_after


@pytest.mark.django_db
class TestCreateOrderProductService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.seller_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        self.token_seller = AuthenticationHelper.register_and_login_user(self.seller_data)
        self.seller = User.objects.get(username=self.seller_data["username"])
        self.service = CreateOrderProductService()
        item_price = 1000
        transaction = Transaction(buyer=self.user, total_price=item_price, date_time=timezone.now(), is_finished=False)
        product = Product(owner=self.seller, name="fefeffe", description="fefeffe", amount=1, price=item_price,
            color="red", weihgt=2, length=3, width=3, height=3, guarantee_period=1, status="available")
        transaction.save()
        product.save()
        self.order_product_creation_data = {"product_id": 1, "transaction_id": 1, "seller_username": self.seller.username,
            "shopping_price": 1000}
        self.created_communicate = "Order created successfully."

    def test_create(self):
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        result = self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert self.created_communicate == result
        assert order_products_before == order_products_after - 1
        assert transactions_before == transactions_after
        assert product.status == "unavailable"

    def test_create_no_transaction(self):
        order_products_before = OrderProduct.objects.count()
        transaction = Transaction.objects.get(transaction_id=1)
        transaction.delete()
        transactions_before = OrderProduct.objects.count()

        result = self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert self.created_communicate == result
        assert order_products_before == order_products_after - 1
        assert transactions_before == transactions_after - 1
        assert product.status == "unavailable"

    def test_create_invalid_transaction_id(self):
        self.order_product_creation_data["transaction_id"] = 2
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Invalid transaction id provided." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "available"

    def test_create_user_is_not_owner_of_transaction(self):
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token_seller, self.seller, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Transaction in which order exists does not belong to the user." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "available"

    def test_create_invalid_product_id(self):
        self.order_product_creation_data["product_id"] = 2
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=2)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Invalid product id provided." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "available"

    def test_create_product_given_self_seller_username(self):
        self.order_product_creation_data["seller_username"] = self.user.username
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Cannot sell product to yourself." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "available"

    def test_create_product_seller_is_not_owner_of_item(self):
        self.seller2_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        AuthenticationHelper.register_and_login_user(self.seller_data)
        seller2 = User.objects.get(username=self.seller_data["username"])
        product = Product(owner=seller2, name="fefeffe", description="fefeffe", amount=1, price=1000,
                          color="red", weihgt=2, length=3, width=3, height=3, guarantee_period=1, status="available")
        product.save()
        self.order_product_creation_data["product_id"] = 2
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Seller is not the owner of this product." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "available"

    def test_create_product_unavailable(self):
        product = Product.objects.get(id=self.order_product_creation_data["product_id"])
        product.status = "unavailable"
        product.save()
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Product is unavailable." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "unavailable"

    def test_create_product_archived(self):
        product = Product.objects.get(id=self.order_product_creation_data["product_id"])
        product.status = "archived"
        product.save()
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Product is archived." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "archived"

    def test_create_invalid_seller_username(self):
        self.order_product_creation_data["seller_username"] = "invalid_username"
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Invalid seller username provided." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "available"

    def test_create_self_seller_username(self):
        self.order_product_creation_data["seller_username"] = self.user.username
        order_products_before = OrderProduct.objects.count()
        transactions_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user, self.order_product_creation_data)
        product = Product.objects.get(id=1)
        order_products_after = OrderProduct.objects.count()
        transactions_after = OrderProduct.objects.count()

        assert "Self username provided." in str(e.value)
        assert order_products_before == order_products_after
        assert transactions_before == transactions_after
        assert product.status == "available"

    def test_create_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.create(access_token, self.user, self.order_product_creation_data)
        order_products_after = OrderProduct.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert order_products_before == order_products_after

    def test_create_incorrect_access_token(self):
        access_token = "invalid token"
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.create(access_token, self.user, self.order_product_creation_data)
        order_products_after = OrderProduct.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert order_products_before == order_products_after

    def test_create_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.create(access_token_first, self.user, self.order_product_creation_data)
            order_products_after = OrderProduct.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert order_products_before == order_products_after


@pytest.mark.django_db
class TestUpdateOrderProductService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.seller_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        self.token_seller = AuthenticationHelper.register_and_login_user(self.seller_data)
        self.seller = User.objects.get(username=self.seller_data["username"])
        item_price = 1000
        transaction = Transaction(buyer=self.user, total_price=item_price, date_time=timezone.now(), is_finished=False)
        product = Product(owner=self.seller, name="fefeffe", description="fefeffe", amount=1, price=item_price, color="red",
            weihgt=2, length=3, width=3, height=3, guarantee_period=1, status="available")
        transaction.save()
        product.save()
        self.order_product = OrderProduct(product=product, transaction=transaction, seller=self.seller, shopping_price=item_price)
        self.order_product.save()
        self.service = UpdateOrderProductService()
        self.order_product_update_data = {"shopping_price": 1000}
        self.updated_communicate = "Order updated successfully"

    def test_update(self):
        order_products_before = OrderProduct.objects.count()

        result = self.service.update(self.token, self.user, self.order_product_update_data)
        order_products_after = OrderProduct.objects.count()

        assert self.updated_communicate == result
        assert order_products_before == order_products_after

    def test_update_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.update(access_token, self.user, self.order_product_update_data)
        order_products_after = OrderProduct.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert order_products_before == order_products_after

    def test_update_incorrect_access_token(self):
        access_token = "invalid token"
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.update(access_token, self.user, self.order_product_update_data)
        order_products_after = OrderProduct.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert order_products_before == order_products_after

    def test_update_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.update(access_token_first, self.user, self.order_product_update_data)
            order_products_after = OrderProduct.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert order_products_before == order_products_after


@pytest.mark.django_db
class TestDeleteOrderProductService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.seller_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                            "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                            "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                            "country": "Poland"}
        self.token_seller = AuthenticationHelper.register_and_login_user(self.seller_data)
        self.seller = User.objects.get(username=self.seller_data["username"])
        item_price = 1000
        transaction = Transaction(buyer=self.user, total_price=item_price, date_time=timezone.now(), is_finished=False)
        product = Product(owner=self.seller, name="fefeffe", description="fefeffe", amount=1, price=item_price, color="red",
            weihgt=2, length=3, width=3, height=3, guarantee_period=1, status="available")
        transaction.save()
        product.save()
        self.order_product = OrderProduct(product=product, transaction=transaction, seller=self.seller, shopping_price=item_price)
        self.order_product.save()
        self.service = DeleteOrderProductService()
        self.order_product_data = {"order_product": 1}

    def test_delete_id(self):
        order_product_id = 1
        order_products_before = OrderProduct.objects.count()

        result = self.service.delete(self.token, self.user, order_product_id)
        status = OrderProduct.objects.get(1).product.status
        order_products_after = OrderProduct.objects.count()

        assert self.order_product_data == result
        assert order_products_before == order_products_after
        assert status == "available"

    def test_delete_id_invalid_id(self):
        order_product_id = 2
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.delete(self.token, self.user, order_product_id)
        status = OrderProduct.objects.get(1).product.status
        order_products_after = OrderProduct.objects.count()

        assert "Order with provided id does not exist." in str(e.value)
        assert order_products_before == order_products_after
        assert status == "available"

    def test_delete_user_is_not_owner_of_transaction(self):
        order_product_id = 1
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.delete(self.token_seller, self.seller, order_product_id)
        status = OrderProduct.objects.get(1).product.status
        order_products_after = OrderProduct.objects.count()

        assert "Transaction in which order exists does not belong to the user." in str(e.value)
        assert order_products_before == order_products_after
        assert status == "available"

    def test_delete_id_expired_access_token(self):
        order_product_id = 1
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.delete(access_token, self.user, order_product_id)
        status = OrderProduct.objects.get(1).product.status
        order_products_after = OrderProduct.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert order_products_before == order_products_after
        assert status == "available"

    def test_delete_incorrect_access_token(self):
        order_product_id = 1
        access_token = "invalid token"
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.delete(access_token, self.user, order_product_id)
        order_products_after = OrderProduct.objects.count()
        status = OrderProduct.objects.get(1).product.status

        assert f"Incorrect access token." in str(e.value)
        assert order_products_before == order_products_after
        assert status == "available"

    def test_delete_expired_by_replacement_access_token(self):
        order_product_id = 1
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        order_products_before = OrderProduct.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.delete(access_token_first, self.user, order_product_id)
        order_products_after = OrderProduct.objects.count()
        status = OrderProduct.objects.get(1).product.status

        assert f"Access token is no longer valid." in str(e.value)
        assert order_products_before == order_products_after
        assert status == "available"
