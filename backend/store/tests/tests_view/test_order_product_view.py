from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import TokenExpiredByReplacementError, CannotGetTokenFromRequestError, TokenExpiredError, \
    IncorrectTokenError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user
from store.helper_tests_classes.order_product_test_helper import OrderProductTestHelper


@pytest.mark.django_db
class TestFindByIdOrderProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.order_product = OrderProductTestHelper.create_order_products(self.user)
        self.ordered_product_id = self.order_product.order_product_id

    @patch("store.service.order_product_service.FindByIdOrderProductService.find_by_id")
    def test_find_by_id_success(self, mock_find_by_id):
        mock_find_by_id.return_value = {"transaction_id": 1, "product_id": 1, "seller_username": "tester2",
            "shopping_price": 1000}

        response = self.client.get(f"/order_product/find_by_id/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["transaction_id"] == 1
        assert response.data["product_id"] == 1
        assert response.data["seller_username"] == "tester2"
        assert response.data["shopping_price"] == 1000
        mock_find_by_id.assert_called_once()

    @patch("store.service.order_product_service.FindByIdOrderProductService.find_by_id")
    def test_find_by_id_invalid_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/order_product/find_by_id/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.FindByIdOrderProductService.find_by_id")
    def test_find_by_id_expired_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/order_product/find_by_id/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.FindByIdOrderProductService.find_by_id")
    def test_find_by_id_cannot_get_token_from_request(self, mock_find_by_id):
        mock_find_by_id.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/order_product/find_by_id/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.FindByIdOrderProductService.find_by_id")
    def test_find_by_id_token_expired_by_replacement(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/order_product/find_by_id/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.FindByIdOrderProductService.find_by_id")
    def test_find_by_id_other_exception(self, mock_find_by_id):
        mock_find_by_id.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/order_product/find_by_id/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.order_product_service.FindByIdOrderProductService.find_by_id")
    def test_find_by_id_invalid_input_data(self, mock_find_by_id):
        mock_find_by_id.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/order_product/find_by_id/{self.ordered_product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_by_id_invalid_serializer(self):
        self.ordered_product_id = -1
        response = self.client.delete(f"/order_product/find_by_id/{self.ordered_product_id}/",
                                      data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCreateOrderProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.data = {"product_id": 1, "seller_username": "tester2", "shopping_price": 2000}

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_success(self, mock_create):
        mock_create.return_value = "Order created successfully."

        response = self.client.post("/order_product/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Order created successfully."
        mock_create.assert_called_once()

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_invalid_token(self, mock_create):
        mock_create.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/order_product/create/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_expired_token(self, mock_create):
        mock_create.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/order_product/create/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_cannot_get_token_from_request(self, mock_create):
        mock_create.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/order_product/create/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_token_expired_by_replacement(self, mock_create):
        mock_create.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/order_product/create/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_other_exception(self, mock_create):
        mock_create.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/order_product/create/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.order_product_service.CreateOrderProductService.create")
    def test_create_invalid_input_data(self, mock_create):
        mock_create.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.post("/order_product/create/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_create_invalid_serializer(self):
        self.data = {}
        response = self.client.put("/order_product/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateOrderProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.order_product = OrderProductTestHelper.create_order_products(self.user)
        self.ordered_product_id = self.order_product.order_product_id
        self.data = {"shopping_price": 2000}

    @patch("store.service.order_product_service.UpdateOrderProductService.update")
    def test_update_success(self, mock_create):
        mock_create.return_value = "Order updated successfully."

        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Order updated successfully."
        mock_create.assert_called_once()

    @patch("store.service.order_product_service.UpdateOrderProductService.update")
    def test_update_invalid_token(self, mock_update):
        mock_update.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.UpdateOrderProductService.update")
    def test_update_expired_token(self, mock_update):
        mock_update.side_effect = TokenExpiredError("Access token error.")

        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.UpdateOrderProductService.update")
    def test_update_cannot_get_token_from_request(self, mock_update):
        mock_update.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.UpdateOrderProductService.update")
    def test_update_token_expired_by_replacement(self, mock_update):
        mock_update.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.UpdateOrderProductService.update")
    def test_update_other_exception(self, mock_update):
        mock_update.side_effect = DatabaseError("DB connection failed")

        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.order_product_service.UpdateOrderProductService.update")
    def test_update_invalid_input_data(self, mock_update):
        mock_update.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_update_invalid_serializer(self):
        self.data = {}
        response = self.client.put("/order_product/update/", data=self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteOrderProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.order_product = OrderProductTestHelper.create_order_products(self.user)
        self.ordered_product_id = self.order_product.order_product_id
        self.data = {"order_product_id": 1}

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_delete_success(self, mock_delete):
        mock_delete.return_value = "Order deleted successfully."

        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/", data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Order deleted successfully."
        mock_delete.assert_called_once()

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_delete_invalid_token(self, mock_delete):
        mock_delete.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/", data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_delete_expired_token(self, mock_delete):
        mock_delete.side_effect = TokenExpiredError("Access token error.")

        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/", data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_delete_cannot_get_token_from_request(self, mock_delete):
        mock_delete.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/", data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_delete_token_expired_by_replacement(self, mock_delete):
        mock_delete.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/", data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_delete_other_exception(self, mock_delete):
        mock_delete.side_effect = DatabaseError("DB connection failed")

        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/", data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.order_product_service.DeleteOrderProductService.delete")
    def test_delete_invalid_input_data(self, mock_delete):
        mock_delete.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/",
            data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_delete_invalid_serializer(self):
        self.ordered_product_id = -1
        response = self.client.delete(f"/order_product/delete/{self.ordered_product_id}/",
                                      data=self.ordered_product_id, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
