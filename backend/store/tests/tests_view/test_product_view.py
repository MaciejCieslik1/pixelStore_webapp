from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user
from store.helper_tests_classes.product_test_helper import ProductTestHelper


@pytest.mark.django_db
class TestFindByIdProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product = ProductTestHelper.create_product(self.user)
        self.product_id = self.product.product_id
        self.product_data = {"product_id": self.product_id, "owner_username": self.product.owner.username,
            "name": self.product.name, "description": self.product.description, "price": self.product.price,
            "amount": self.product.amount, "color": self.product.color, "weight": self.product.weight,
            "length": self.product.length, "width": self.product.width, "height": self.product.height,
            "guarantee_period": self.product.guarantee_period, "status": self.product.status}

    @patch("store.service.product_service.FindByIdProductService.find_by_id")
    def test_find_by_id_success(self, mock_find_by_id):
        mock_find_by_id.return_value = self.product_data

        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.product_data
        mock_find_by_id.assert_called_once()

    @patch("store.service.product_service.FindByIdProductService.find_by_id")
    def test_find_by_id_invalid_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindByIdProductService.find_by_id")
    def test_find_by_id_expired_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindByIdProductService.find_by_id")
    def test_find_by_id_cannot_get_token_from_request(self, mock_find_by_id):
        mock_find_by_id.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindByIdProductService.find_by_id")
    def test_find_by_id_token_expired_by_replacement(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindByIdProductService.find_by_id")
    def test_find_by_id_other_exception(self, mock_find_by_id):
        mock_find_by_id.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_service.FindByIdProductService.find_by_id")
    def test_find_by_id_invalid_input_data(self, mock_find_by_id):
        mock_find_by_id.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_by_id_invalid_serializer(self):
        self.product_id = 0
        response = self.client.get(f"/product/find_by_id/{self.product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestFindAllProducts:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product = ProductTestHelper.create_product(self.user)
        self.product_id = self.product.product_id
        self.products_data = [{"product_id": self.product_id, "owner_username": self.product.owner.username,
            "name": self.product.name, "description": self.product.description, "price": self.product.price,
            "amount": self.product.amount, "color": self.product.color, "weight": self.product.weight,
            "length": self.product.length, "width": self.product.width, "height": self.product.height,
            "guarantee_period": self.product.guarantee_period, "status": self.product.status}]

    @patch("store.service.product_service.FindAllProductsService.find_all")
    def test_find_all_success(self, mock_find_all):
        mock_find_all.return_value = self.products_data

        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.products_data
        mock_find_all.assert_called_once()

    @patch("store.service.product_service.FindAllProductsService.find_all")
    def test_find_all_invalid_token(self, mock_find_all):
        mock_find_all.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindAllProductsService.find_all")
    def test_find_all_expired_token(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindAllProductsService.find_all")
    def test_find_all_cannot_get_token_from_request(self, mock_find_all):
        mock_find_all.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindAllProductsService.find_all")
    def test_find_all_token_expired_by_replacement(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.FindAllProductsService.find_all")
    def test_find_all_other_exception(self, mock_find_all):
        mock_find_all.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_service.FindAllProductsService.find_all")
    def test_find_all_invalid_input_data(self, mock_find_all):
        mock_find_all.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_all_invalid_serializer(self):
        self.product_id = 0
        response = self.client.get(f"/product/find_all/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCreateProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product = ProductTestHelper.create_product(self.user)
        self.product_id = self.product.product_id
        self.product_creation_data = {"owner_username": self.product.owner.username,
            "name": self.product.name, "description": self.product.description, "price": self.product.price,
            "amount": self.product.amount, "color": self.product.color, "weight": self.product.weight,
            "length": self.product.length, "width": self.product.width, "height": self.product.height,
            "guarantee_period": self.product.guarantee_period, "status": self.product.status}
        self.product_communicate = "Product created successfully."

    @patch("store.service.product_service.CreateProductService.create")
    def test_create_success(self, mock_create):
        mock_create.return_value = self.product_communicate

        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.product_communicate
        mock_create.assert_called_once()

    @patch("store.service.product_service.CreateProductService.create")
    def test_create_invalid_token(self, mock_create):
        mock_create.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.CreateProductService.create")
    def test_create_expired_token(self, mock_create):
        mock_create.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.CreateProductService.create")
    def test_create_cannot_get_token_from_request(self, mock_create):
        mock_create.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.CreateProductService.create")
    def test_create_token_expired_by_replacement(self, mock_create):
        mock_create.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.CreateProductService.create")
    def test_create_other_exception(self, mock_create):
        mock_create.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_service.CreateProductService.create")
    def test_create_invalid_input_data(self, mock_create):
        mock_create.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Invalid input data provided."

    def test_create_invalid_serializer(self):
        self.product_id = 0
        response = self.client.post("/product/create/", data=self.product_creation_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product = ProductTestHelper.create_product(self.user)
        self.product_id = self.product.product_id
        self.product_communicate = "Product updated successfully."

    @patch("store.service.product_service.UpdateProductService.update")
    def test_update_success(self, mock_update):
        mock_update.return_value = self.product_communicate

        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.product_communicate
        mock_update.assert_called_once()

    @patch("store.service.product_service.UpdateProductService.update")
    def test_update_invalid_token(self, mock_update):
        mock_update.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.UpdateProductService.update")
    def test_update_expired_token(self, mock_update):
        mock_update.side_effect = TokenExpiredError("Access token error.")

        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.UpdateProductService.update")
    def test_find_by_id_cannot_get_token_from_request(self, mock_update):
        mock_update.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.UpdateProductService.update")
    def test_update_token_expired_by_replacement(self, mock_update):
        mock_update.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.UpdateProductService.update")
    def test_find_by_id_other_exception(self, mock_update):
        mock_update.side_effect = DatabaseError("DB connection failed")

        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_service.UpdateProductService.update")
    def test_update_invalid_input_data(self, mock_update):
        mock_update.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_update_invalid_serializer(self):
        self.product_id = 0
        response = self.client.put(f"/product/update/{self.product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product = ProductTestHelper.create_product(self.user)
        self.product_id = self.product.product_id
        self.product_communicate = "Product deleted successfully."

    @patch("store.service.product_service.DeleteProductService.delete")
    def test_delete_success(self, mock_delete):
        mock_delete.return_value = self.product_communicate

        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.product_communicate
        mock_delete.assert_called_once()

    @patch("store.service.product_service.DeleteProductService.delete")
    def test_delete_invalid_token(self, mock_delete):
        mock_delete.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.DeleteProductService.delete")
    def test_delete_expired_token(self, mock_delete):
        mock_delete.side_effect = TokenExpiredError("Access token error.")

        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.DeleteProductService.delete")
    def test_delete_cannot_get_token_from_request(self, mock_delete):
        mock_delete.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.DeleteProductService.delete")
    def test_delete_token_expired_by_replacement(self, mock_delete):
        mock_delete.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_service.DeleteProductService.delete")
    def test_delete_other_exception(self, mock_delete):
        mock_delete.side_effect = DatabaseError("DB connection failed")

        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_service.DeleteProductService.delete")
    def test_delete_invalid_input_data(self, mock_delete):
        mock_delete.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_delete_invalid_serializer(self):
        self.product_id = 0
        response = self.client.delete(f"/product/delete/{self.product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
