from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user
from store.helper_tests_classes.product_photo_test_helper import ProductPhotoTestHelper


@pytest.mark.django_db
class TestFindByIdProductPhoto:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product_photo = ProductPhotoTestHelper.create_product_photo(self.user)
        self.product_photo_id = self.product_photo.product_photo_id
        self.product_photo_data = {"product_photo_id": self.product_photo_id,
            "product_id": self.product_photo.product.product_id, "image_url": self.product_photo.image_url,
            "is_main_photo": self.product_photo.is_main_photo}

    @patch("store.service.product_photo_service.FindByIdProductPhotoService.find_by_id")
    def test_find_by_id_success(self, mock_find_by_id):
        mock_find_by_id.return_value = self.product_photo_data

        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.product_photo_data
        mock_find_by_id.assert_called_once()

    @patch("store.service.product_photo_service.FindByIdProductPhotoService.find_by_id")
    def test_find_by_id_invalid_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindByIdProductPhotoService.find_by_id")
    def test_find_by_id_expired_token(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindByIdProductPhotoService.find_by_id")
    def test_find_by_id_cannot_get_token_from_request(self, mock_find_by_id):
        mock_find_by_id.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindByIdProductPhotoService.find_by_id")
    def test_find_by_id_token_expired_by_replacement(self, mock_find_by_id):
        mock_find_by_id.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindByIdProductPhotoService.find_by_id")
    def test_find_by_id_other_exception(self, mock_find_by_id):
        mock_find_by_id.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_photo_service.FindByIdProductPhotoService.find_by_id")
    def test_find_by_id_invalid_input_data(self, mock_find_by_id):
        mock_find_by_id.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_by_id_invalid_serializer(self):
        self.product_photo_id = 0
        response = self.client.get(f"/product_photo/find_by_id/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestFindAllProductPhotos:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product_photo = ProductPhotoTestHelper.create_product_photo(self.user)
        self.product_photo_id = self.product_photo.product_photo_id
        self.product_id = self.product_photo.product.product_id
        self.product_photos_data = [{"product_photo_id": self.product_photo_id,
            "product_id": self.product_photo.product.product_id, "image_url": self.product_photo.image_url,
            "is_main_photo": self.product_photo.is_main_photo}]

    @patch("store.service.product_photo_service.FindAllForProductService.find_all_for_product")
    def test_find_all_for_product_success(self, mock_find_all):
        mock_find_all.return_value = self.product_photos_data

        response = self.client.get(f"/product_photo/find_all_for_product/{self.product_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.product_photos_data
        mock_find_all.assert_called_once()

    @patch("store.service.product_photo_service.FindAllForProductService.find_all_for_product")
    def test_find_all_for_product_invalid_token(self, mock_find_all):
        mock_find_all.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/product_photo/find_all_for_product/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindAllForProductService.find_all_for_product")
    def test_find_all_for_product_expired_token(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/product_photo/find_all_for_product/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindAllForProductService.find_all_for_product")
    def test_find_all_for_product_cannot_get_token_from_request(self, mock_find_all):
        mock_find_all.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/product_photo/find_all_for_product/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindAllForProductService.find_all_for_product")
    def test_find_all_for_product_token_expired_by_replacement(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/product_photo/find_all_for_product/{self.product_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.FindAllForProductService.find_all_for_product")
    def test_find_all_for_product_other_exception(self, mock_find_all):
        mock_find_all.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/product_photo/find_all_for_product/{self.product_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_photo_service.FindAllForProductService.find_all_for_product")
    def test_find_all_for_product_invalid_input_data(self, mock_find_all):
        mock_find_all.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/product_photo/find_all_for_product/{self.product_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."


@pytest.mark.django_db
class TestCreateProductPhoto:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product_photo = ProductPhotoTestHelper.create_product_photo(self.user)
        self.product_photo_id = self.product_photo.product_photo_id
        self.product_photo_creation_data = {"product_photo_id": self.product_photo_id,
            "product_id": self.product_photo.product.product_id,
           "image_url": self.product_photo.image_url,
           "is_main_photo": self.product_photo.is_main_photo}

        self.product_photo_communicate = "Product photo created successfully."

    @patch("store.service.product_photo_service.CreateProductPhotoService.create")
    def test_create_success(self, mock_create):
        mock_create.return_value = self.product_photo_communicate

        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.product_photo_communicate
        mock_create.assert_called_once()

    @patch("store.service.product_photo_service.CreateProductPhotoService.create")
    def test_create_invalid_token(self, mock_create):
        mock_create.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.CreateProductPhotoService.create")
    def test_create_expired_token(self, mock_create):
        mock_create.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.CreateProductPhotoService.create")
    def test_create_cannot_get_token_from_request(self, mock_create):
        mock_create.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.CreateProductPhotoService.create")
    def test_create_token_expired_by_replacement(self, mock_create):
        mock_create.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.CreateProductPhotoService.create")
    def test_create_other_exception(self, mock_create):
        mock_create.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_photo_service.CreateProductPhotoService.create")
    def test_create_invalid_input_data(self, mock_create):
        mock_create.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Invalid input data provided."

    def test_create_invalid_serializer(self):
        self.product_photo_creation_data["product_id"] = 0
        response = self.client.post("/product_photo/create/", data=self.product_photo_creation_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteProductPhoto:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.product_photo = ProductPhotoTestHelper.create_product_photo(self.user)
        self.product_photo_id = self.product_photo.product_photo_id
        self.product_communicate = "Product photo deleted successfully"

    @patch("store.service.product_photo_service.DeleteProductPhotoService.delete")
    def test_delete_success(self, mock_delete):
        mock_delete.return_value = self.product_communicate

        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.product_communicate
        mock_delete.assert_called_once()

    @patch("store.service.product_photo_service.DeleteProductPhotoService.delete")
    def test_delete_invalid_token(self, mock_delete):
        mock_delete.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.DeleteProductPhotoService.delete")
    def test_delete_expired_token(self, mock_delete):
        mock_delete.side_effect = TokenExpiredError("Access token error.")

        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.DeleteProductPhotoService.delete")
    def test_delete_cannot_get_token_from_request(self, mock_delete):
        mock_delete.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.DeleteProductPhotoService.delete")
    def test_delete_token_expired_by_replacement(self, mock_delete):
        mock_delete.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.product_photo_service.DeleteProductPhotoService.delete")
    def test_delete_other_exception(self, mock_delete):
        mock_delete.side_effect = DatabaseError("DB connection failed")

        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.product_photo_service.DeleteProductPhotoService.delete")
    def test_delete_invalid_input_data(self, mock_delete):
        mock_delete.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_delete_invalid_serializer(self):
        self.product_photo_id = 0
        response = self.client.delete(f"/product_photo/delete/{self.product_photo_id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
