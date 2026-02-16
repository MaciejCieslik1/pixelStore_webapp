from decimal import Decimal
from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user
from store.helper_tests_classes.product_test_helper import ProductTestHelper
from store.helper_tests_classes.transaction_test_helper import TransactionTestHelper


@pytest.mark.django_db
class TestFindByIdTransaction:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.transaction = TransactionTestHelper.create_transaction(self.user)
        self.transaction_data = {"transaction_id": self.transaction.transaction_id,
            "buyer_username": self.transaction.buyer.username, "total_price": self.transaction.total_price,
            "date_time": self.transaction.date_time, "is_finished": self.transaction.is_finished}

    @patch("store.service.transaction_service.FindByIdTransactionService.find_by_id")
    def test_find_by_id_success(self, mock_find_by_id):
        mock_find_by_id.return_value = self.transaction_data

        response = self.client.get(f"/transaction/find_by_id/{self.transaction.transaction_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.transaction_data
        mock_find_by_id.assert_called_once()

    @patch("store.service.transaction_service.FindByIdTransactionService.find_by_id")
    def test_find_by_id_invalid_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/transaction/find_by_id/{self.transaction.transaction_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindByIdTransactionService.find_by_id")
    def test_find_by_id_expired_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/transaction/find_by_id/{self.transaction.transaction_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindByIdTransactionService.find_by_id")
    def test_find_by_id_cannot_get_token_from_request(self, mock_find_by_id):
        mock_find_by_id.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/transaction/find_by_id/{self.transaction.transaction_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindByIdTransactionService.find_by_id")
    def test_find_by_id_token_expired_by_replacement(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/transaction/find_by_id/{self.transaction.transaction_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindByIdTransactionService.find_by_id")
    def test_find_by_id_other_exception(self, mock_find_by_id):
        mock_find_by_id.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/transaction/find_by_id/{self.transaction.transaction_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.transaction_service.FindByIdTransactionService.find_by_id")
    def test_find_by_id_invalid_input_data(self, mock_find_by_id):
        mock_find_by_id.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/transaction/find_by_id/{self.transaction.transaction_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_by_id_invalid_serializer(self):
        transaction_id = 0
        response = self.client.get(f"/transaction/find_by_id/{transaction_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestFindAllTransaction:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product = ProductTestHelper.create_product(self.user)
        self.transaction1 = TransactionTestHelper.create_transaction(self.user)
        self.transaction1_data = {"transaction_id": self.transaction1.transaction_id,
                                 "buyer_username": self.transaction1.buyer.username,
                                 "total_price": self.transaction1.total_price,
                                 "date_time": self.transaction1.date_time,
                                  "is_finished": self.transaction1.is_finished}
        self.transaction2 = TransactionTestHelper.create_transaction(self.user)
        self.transaction2_data = {"transaction_id": self.transaction2.transaction_id,
                                  "buyer_username": self.transaction2.buyer.username,
                                  "total_price": self.transaction2.total_price,
                                  "date_time": self.transaction2.date_time,
                                  "is_finished": self.transaction2.is_finished}
        self.transactions_data = [self.transaction1_data, self.transaction2_data]


    @patch("store.service.transaction_service.FindAllMineTransactionsService.find_all_mine")
    def test_find_all_mine_transactions_success(self, mock_find_all):
        mock_find_all.return_value = self.transactions_data

        response = self.client.get(f"/transaction/find_all_mine/", {"page": 1, "page_size": 10})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.transactions_data
        mock_find_all.assert_called_once()

    @patch("store.service.transaction_service.FindAllMineTransactionsService.find_all_mine")
    def test_find_all_mine_transactions_invalid_token(self, mock_find_all):
        mock_find_all.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/transaction/find_all_mine/", {"page": 1, "page_size": 10})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindAllMineTransactionsService.find_all_mine")
    def test_find_all_mine_transactions_expired_token(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/transaction/find_all_mine/", {"page": 1, "page_size": 10})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindAllMineTransactionsService.find_all_mine")
    def test_find_all_mine_transactions_cannot_get_token_from_request(self, mock_find_all):
        mock_find_all.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/transaction/find_all_mine/", {"page": 1, "page_size": 10})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindAllMineTransactionsService.find_all_mine")
    def test_find_all_mine_transactions_token_expired_by_replacement(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/transaction/find_all_mine/", {"page": 1, "page_size": 10})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.FindAllMineTransactionsService.find_all_mine")
    def test_find_all_mine_transactions_other_exception(self, mock_find_all):
        mock_find_all.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/transaction/find_all_mine/", {"page": 1, "page_size": 10})

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.transaction_service.FindAllMineTransactionsService.find_all_mine")
    def test_find_all_mine_transactions_invalid_input_data(self, mock_find_all):
        mock_find_all.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/transaction/find_all_mine/", {"page": 1, "page_size": 10})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."


@pytest.mark.django_db
class TestCreateTransaction:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.transaction_creation_data = {"buyer_username": self.user.username, "total_price": Decimal("100")}
        self.transaction_communicate = "Transaction created successfully."

    @patch("store.service.transaction_service.CreateTransactionService.create")
    def test_create_success(self, mock_create):
        mock_create.return_value = self.transaction_communicate

        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.transaction_communicate
        mock_create.assert_called_once()

    @patch("store.service.transaction_service.CreateTransactionService.create")
    def test_create_invalid_token(self, mock_create):
        mock_create.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.CreateTransactionService.create")
    def test_create_expired_token(self, mock_create):
        mock_create.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.CreateTransactionService.create")
    def test_create_cannot_get_token_from_request(self, mock_create):
        mock_create.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.CreateTransactionService.create")
    def test_create_token_expired_by_replacement(self, mock_create):
        mock_create.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.CreateTransactionService.create")
    def test_create_other_exception(self, mock_create):
        mock_create.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.transaction_service.CreateTransactionService.create")
    def test_create_invalid_input_data(self, mock_create):
        mock_create.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Invalid input data provided."

    def test_create_invalid_serializer(self):
        self.transaction_creation_data["total_price"] = Decimal("0")
        response = self.client.post("/transaction/create/", data=self.transaction_creation_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateTransaction:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.transaction_update_data = {"total_price": Decimal("100"), "is_finished": False}
        self.transaction_id = 1
        self.transaction_communicate = "Transaction updated successfully."

    @patch("store.service.transaction_service.UpdateTransactionService.update")
    def test_update_success(self, mock_update):
        mock_update.return_value = self.transaction_communicate

        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.transaction_communicate
        mock_update.assert_called_once()

    @patch("store.service.transaction_service.UpdateTransactionService.update")
    def test_update_invalid_token(self, mock_update):
        mock_update.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.UpdateTransactionService.update")
    def test_update_expired_token(self, mock_update):
        mock_update.side_effect = TokenExpiredError("Access token error.")

        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.UpdateTransactionService.update")
    def test_update_cannot_get_token_from_request(self, mock_update):
        mock_update.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.UpdateTransactionService.update")
    def test_update_token_expired_by_replacement(self, mock_update):
        mock_update.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.transaction_service.UpdateTransactionService.update")
    def test_update_other_exception(self, mock_update):
        mock_update.side_effect = DatabaseError("DB connection failed")

        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.transaction_service.UpdateTransactionService.update")
    def test_update_invalid_input_data(self, mock_update):
        mock_update.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_update_invalid_serializer(self):
        self.transaction_update_data["total_price"] = Decimal("0")
        response = self.client.put(f"/transaction/update/{self.transaction_id}/", data=self.transaction_update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
