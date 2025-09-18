from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import TokenExpiredByReplacementError, CannotGetTokenFromRequestError, TokenExpiredError, \
    IncorrectTokenError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user
from store.helper_tests_classes.order_return_test_helper import OrderReturnTestHelper


@pytest.mark.django_db
class TestFindByIdOrderReturn:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.order_return = OrderReturnTestHelper.create_order_return(self.user)
        self.ordered_return_id = self.order_return.order_return_id

    @patch("store.service.order_return_service.FindByIdOrderReturnService.find_by_id")
    def test_find_by_id_success(self, mock_find_by_id):
        mock_find_by_id.return_value = {"order_return_id": self.ordered_return_id,
            "order_product_id": self.order_return.order_product.order_product_id, "description": self.order_return.description,
            "return_date_time": self.order_return.return_date_time, "is_accepted": self.order_return.is_accepted}

        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["order_return_id"] == self.ordered_return_id
        assert response.data["order_product_id"] == self.order_return.order_product.order_product_id
        assert response.data["description"] == self.order_return.description
        assert response.data["return_date_time"] == self.order_return.return_date_time
        assert response.data["is_accepted"] == self.order_return.is_accepted
        mock_find_by_id.assert_called_once()

    @patch("store.service.order_return_service.FindByIdOrderReturnService.find_by_id")
    def test_find_by_id_invalid_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_return_service.FindByIdOrderReturnService.find_by_id")
    def test_find_by_id_expired_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_return_service.FindByIdOrderReturnService.find_by_id")
    def test_find_by_id_cannot_get_token_from_request(self, mock_find_by_id):
        mock_find_by_id.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_return_service.FindByIdOrderReturnService.find_by_id")
    def test_find_by_id_token_expired_by_replacement(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_return_service.FindByIdOrderReturnService.find_by_id")
    def test_find_by_id_other_exception(self, mock_find_by_id):
        mock_find_by_id.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.order_return_service.FindByIdOrderReturnService.find_by_id")
    def test_find_by_id_invalid_input_data(self, mock_find_by_id):
        mock_find_by_id.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_by_id_invalid_serializer(self):
        self.ordered_return_id = 0
        response = self.client.get(f"/order_return/find_by_id/{self.ordered_return_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCreateOrderProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.data = {"order_product_id": 1, "description": "example_description"}

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_success(self, mock_create):
        mock_create.return_value = "Order return created successfully."

        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Order return created successfully."
        mock_create.assert_called_once()

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_invalid_token(self, mock_create):
        mock_create.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_expired_token(self, mock_create):
        mock_create.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_cannot_get_token_from_request(self, mock_create):
        mock_create.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_token_expired_by_replacement(self, mock_create):
        mock_create.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_other_exception(self, mock_create):
        mock_create.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_invalid_input_data(self, mock_create):
        mock_create.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_create_invalid_serializer(self):
        self.data = {}
        response = self.client.post("/order_return/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateOrderProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.order_return = OrderReturnTestHelper.create_order_return(self.user)
        self.ordered_return_id = self.order_return.order_return_id
        self.data = {"order_product_id": self.order_return.order_return_id}

    @patch("store.service.order_return_service.UpdateOrderReturnService.update")
    def test_update_success(self, mock_update):
        mock_update.return_value = "Order return updated successfully."

        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Order updated successfully."
        mock_update.assert_called_once()

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_update_invalid_token(self, mock_update):
        mock_update.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_update_expired_token(self, mock_update):
        mock_update.side_effect = TokenExpiredError("Access token error.")

        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_update_cannot_get_token_from_request(self, mock_update):
        mock_update.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_update_token_expired_by_replacement(self, mock_update):
        mock_update.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_update_other_exception(self, mock_update):
        mock_update.side_effect = DatabaseError("DB connection failed")

        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_update_invalid_input_data(self, mock_update):
        mock_update.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_update_invalid_serializer(self):
        self.ordered_product_id = 0
        response = self.client.update(f"/order_return/update/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
