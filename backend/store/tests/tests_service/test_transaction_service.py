from decimal import Decimal

import pytest
from store.exceptions import InvalidInputData
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.helper_tests_classes.product_test_helper import ProductTestHelper
from store.helper_tests_classes.transaction_test_helper import TransactionTestHelper
from store.models import User, ProductReview, Transaction, OrderProduct
from store.service.transaction_service import FindByIdTransactionService, FindAllMineTransactionsService, \
    CreateTransactionService, UpdateTransactionService


@pytest.mark.django_db
class TestFindByIdTransactionService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.user_data2 = AuthenticationHelper.return_exemplary_user_data()
        self.user_data2["username"] = "tester10"
        self.user_data2["email"] = "test10@example.com"
        AuthenticationHelper.register_and_login_user(self.user_data2)
        self.user2 = User.objects.get(username=self.user_data2["username"])
        self.transaction = TransactionTestHelper.create_transaction(self.user2)
        self.transaction_id = self.transaction.transaction_id
        self.transaction_dict = {
            "transaction_id": self.transaction.transaction_id,
            "buyer_username": self.transaction.buyer.username,
            "total_price": f"{self.transaction.total_price:.2f}",
            "date_time": self.transaction.date_time.isoformat().replace("+00:00", "Z"),
            "is_finished": self.transaction.is_finished,
        }
        self.product = ProductTestHelper.create_product(self.owner)
        self.order_product = OrderProduct(transaction=self.transaction, product=self.product, seller=self.owner,
                                          shopping_price=Decimal("1000"))
        self.order_product.save()
        self.service = FindByIdTransactionService()


    def test_find_by_id(self):
        transaction_before = Transaction.objects.all().count()
        result = self.service.find_by_id(self.token, self.owner, self.transaction_id)
        transaction_after = Transaction.objects.all().count()

        assert result == self.transaction_dict
        assert transaction_before == transaction_after


    def test_find_by_id_buyer(self):
        transaction_before = Transaction.objects.all().count()
        result = self.service.find_by_id(self.token, self.user2, self.transaction_id)
        transaction_after = Transaction.objects.all().count()

        assert result == self.transaction_dict
        assert transaction_before == transaction_after


    def test_find_by_id_invalid_id(self):
        transaction_before = Transaction.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token, self.owner, self.transaction_id + 10)
        transaction_after = Transaction.objects.all().count()

        assert f"Transaction with this id does not exist." in str(e.value)
        assert transaction_before == transaction_after


    def test_find_by_id_transaction_does_not_belong_to_user(self):
        user3_data = AuthenticationHelper.return_exemplary_user_data()
        user3_data["username"] = "tester11"
        user3_data["email"] = "tester11@gmail.com"
        AuthenticationHelper.register_and_login_user(user3_data)
        user3 = User.objects.get(username=user3_data["username"])
        transaction_before = Transaction.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token, user3, self.transaction_id)
        transaction_after = Transaction.objects.all().count()

        assert f"Transaction with this id does not belong to the user." in str(e.value)
        assert transaction_before == transaction_after


@pytest.mark.django_db
class TestFindAllMineTransactionsService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        user2_data = AuthenticationHelper.return_exemplary_user_data()
        user2_data["username"] = "tester12"
        user2_data["email"] = "tester12@gmail.com"
        AuthenticationHelper.register_and_login_user(user2_data)
        user2 = User.objects.get(username=user2_data["username"])
        self.transaction1 = TransactionTestHelper.create_transaction(self.owner)
        self.transaction2 = TransactionTestHelper.create_transaction(self.owner)
        self.transaction3 = TransactionTestHelper.create_transaction(user2)
        self.transaction_dict1 = {
            "transaction_id": self.transaction1.transaction_id,
            "buyer_username": self.transaction1.buyer.username,
            "total_price": str(self.transaction1.total_price),
            "date_time": self.transaction1.date_time,
            "is_finished": self.transaction1.is_finished,
        }
        self.transaction_dict2 = {
            "transaction_id": self.transaction2.transaction_id,
            "buyer_username": self.transaction2.buyer.username,
            "total_price": str(self.transaction2.total_price),
            "date_time": self.transaction2.date_time,
            "is_finished": self.transaction2.is_finished,
        }
        self.transaction_dict3 = {
            "transaction_id": self.transaction3.transaction_id,
            "buyer_username": self.transaction3.buyer.username,
            "total_price": str(self.transaction3.total_price),
            "date_time": self.transaction3.date_time,
            "is_finished": self.transaction3.is_finished,
        }
        user3_data = AuthenticationHelper.return_exemplary_user_data()
        user3_data["username"] = "tester13"
        user3_data["email"] = "tester13@gmail.com"
        AuthenticationHelper.register_and_login_user(user3_data)
        user3 = User.objects.get(username=user3_data["username"])
        self.transactions = [self.transaction_dict1, self.transaction_dict2, self.transaction_dict3]
        self.product = ProductTestHelper.create_product(self.owner)
        self.order_product1 = OrderProduct(transaction=self.transaction1, product=self.product, seller=user2,
                                          shopping_price=Decimal("1000"))
        self.order_product1.save()
        self.order_product2 = OrderProduct(transaction=self.transaction2, product=self.product, seller=user2,
                                          shopping_price=Decimal("1000"))
        self.order_product2.save()
        self.order_product3 = OrderProduct(transaction=self.transaction3, product=self.product, seller=user3,
                                          shopping_price=Decimal("1000"))
        self.order_product3.save()
        self.service = FindAllMineTransactionsService()


    def test_find_all_mine(self):
        transaction_find_data = {"page": 1, "page_size": 10}
        transactions_before = Transaction.objects.all().count()
        result = self.service.find_all_mine(self.token, self.owner, transaction_find_data)
        transactions_after = Transaction.objects.all().count()

        assert len(result) == len(self.transactions) - 1
        assert transactions_before == transactions_after


@pytest.mark.django_db
class TestCreateTransactionService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.user_data2 = AuthenticationHelper.return_exemplary_user_data()
        self.user_data2["username"] = "tester14"
        self.user_data2["email"] = "tester14@example.com"
        AuthenticationHelper.register_and_login_user(self.user_data2)
        self.user2 = User.objects.get(username=self.user_data2["username"])
        self.create_transaction_dict = {"buyer_username": "tester14", "total_price": Decimal("1000")}
        self.service = CreateTransactionService()


    def test_create(self):
        transactions_before = Transaction.objects.all().count()
        result = self.service.create(self.token, self.owner, self.create_transaction_dict)
        transactions_after = Transaction.objects.all().count()

        assert result == "Transaction created successfully."
        assert transactions_before == transactions_after - 1


    def test_create_invalid_buyer_username(self):
        transactions_before = Transaction.objects.all().count()
        self.create_transaction_dict["buyer_username"] = "tester3"
        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.owner, self.create_transaction_dict)
        transactions_after = Transaction.objects.all().count()

        assert f"User with this username does not exist." in str(e.value)
        assert transactions_before == transactions_after


@pytest.mark.django_db
class TestUpdateTransactionService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.user_data2 = AuthenticationHelper.return_exemplary_user_data()
        self.user_data2["username"] = "tester15"
        self.user_data2["email"] = "tester15@example.com"
        AuthenticationHelper.register_and_login_user(self.user_data2)
        self.user2 = User.objects.get(username=self.user_data2["username"])
        self.user2.money = Decimal("1000")
        self.user2.save()
        self.owner.money = Decimal("1000")
        self.owner.save()
        self.product = ProductTestHelper.create_product(self.owner)
        self.transaction = TransactionTestHelper.create_transaction(self.user2)
        self.transaction_id = self.transaction.transaction_id
        self.order_product = OrderProduct(transaction=self.transaction, product=self.product, seller=self.owner,
                                          shopping_price=Decimal("1000"))
        self.order_product.save()
        self.service = UpdateTransactionService()


    def test_update(self):
        transactions_before = ProductReview.objects.all().count()
        owner_money_before = self.owner.money
        buyer_money_before = self.user2.money
        result = self.service.update(self.token, self.user2, self.transaction_id)
        owner = User.objects.get(username=self.user_data["username"])
        user2 = User.objects.get(username=self.user_data2["username"])
        transactions_after = ProductReview.objects.all().count()
        owner_money_after = owner.money
        buyer_money_after = user2.money
        transaction = Transaction.objects.filter(transaction_id=self.transaction_id).first()

        assert result == "Transaction updated successfully."
        assert transaction.is_finished == True
        assert transactions_before == transactions_after
        assert owner_money_before == owner_money_after - self.transaction.total_price
        assert buyer_money_before == buyer_money_after + self.transaction.total_price


    def test_update_invalid_transaction_id(self):
        transactions_before = ProductReview.objects.all().count()
        owner_money_before = self.owner.money
        buyer_money_before = self.user2.money
        with pytest.raises(InvalidInputData) as e:
            self.service.update(self.token, self.owner, self.transaction_id + 10)
        transactions_after = ProductReview.objects.all().count()
        owner_money_after = self.owner.money
        buyer_money_after = self.user2.money

        assert f"Transaction with this id does not exist." in str(e.value)
        assert transactions_before == transactions_after
        assert owner_money_before == owner_money_after
        assert buyer_money_before == buyer_money_after


    def test_update_transaction_finished(self):
        transaction = TransactionTestHelper.create_transaction(self.user2)
        transaction_id = transaction.transaction_id
        transactions_before = ProductReview.objects.all().count()
        owner_money_before = self.owner.money
        buyer_money_before = self.user2.money
        transaction.is_finished = True
        transaction.save()
        with pytest.raises(InvalidInputData) as e:
            self.service.update(self.token, self.user2, transaction_id)
        transactions_after = ProductReview.objects.all().count()
        owner_money_after = self.owner.money
        buyer_money_after = self.user2.money

        assert f"Transaction with this id is already finished." in str(e.value)
        assert transactions_before == transactions_after
        assert owner_money_before == owner_money_after
        assert buyer_money_before == buyer_money_after


    def test_update_not_owner(self):
        transactions_before = ProductReview.objects.all().count()
        owner_money_before = self.owner.money
        buyer_money_before = self.user2.money
        with pytest.raises(InvalidInputData) as e:
            self.service.update(self.token, self.owner, self.transaction_id)
        transactions_after = ProductReview.objects.all().count()
        owner_money_after = self.owner.money
        buyer_money_after = self.user2.money

        assert f"Transaction with this id does not belong to the user." in str(e.value)
        assert transactions_before == transactions_after
        assert owner_money_before == owner_money_after
        assert buyer_money_before == buyer_money_after
