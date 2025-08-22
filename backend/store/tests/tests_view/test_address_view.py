from unittest.mock import patch
import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import TokenExpiredError, IncorrectTokenError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError
from store.helper_tests_classes.address_test_helper import AddressTestHelper
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user
from store.models import Address


@pytest.mark.django_db
class TestFindAddress:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.address_data = {"address": "example_street", "postal_code": "00001", "city": "Warsaw",
                             "country": "Poland"}
        address = Address.create_address(self.address_data, self.user)
        address.save()

    @patch("store.service.address_service.FindAddressService.find")
    def test_find_address_success(self, mock_find_address):
        mock_find_address.return_value = {"address": "example_street", "postal_code": "00001", "city": "Warsaw",
                                          "country": "Poland"}

        response = self.client.get("/address/find/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["address"] == "example_street"
        assert response.data["postal_code"] == "00001"
        assert response.data["city"] == "Warsaw"
        assert response.data["country"] == "Poland"
        mock_find_address.assert_called_once()

    @patch("store.service.address_service.FindAddressService.find")
    def test_find_address_invalid_token(self, mock_find_address):
        mock_find_address.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get("/address/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.FindAddressService.find")
    def test_find_address_expired_token(self, mock_find_address):
        mock_find_address.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get("/address/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.FindAddressService.find")
    def test_find_address_cannot_get_token_from_request(self, mock_find_address):
        mock_find_address.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get("/address/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.FindAddressService.find")
    def test_find_address_token_expired_by_replacement(self, mock_find_address):
        mock_find_address.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get("/address/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.FindAddressService.find")
    def test_find_address_other_exception(self, mock_find_address):
        mock_find_address.side_effect = DatabaseError("DB connection failed")

        response = self.client.get("/address/find/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."


@pytest.mark.django_db
class TestUpdateAddress:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        AddressTestHelper.create_address(self.user)
        self.updated_address = {"address": "example_street2", "postal_code": "00002", "city": "London",
                             "country": "UK"}

    @patch("store.service.address_service.UpdateAddressService.update")
    def test_update_address_success(self, mock_update_address):
        mock_update_address.return_value = "Address successfully updated."

        response = self.client.put("/address/update/", self.updated_address, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Address successfully updated."
        mock_update_address.assert_called_once()

    @patch("store.service.address_service.UpdateAddressService.update")
    def test_update_address_invalid_token(self, mock_update_address):
        mock_update_address.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.put("/address/update/", self.updated_address, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.UpdateAddressService.update")
    def test_update_address_expired_token(self, mock_update_address):
        mock_update_address.side_effect = TokenExpiredError("Access token error.")

        response = self.client.put("/address/update/", self.updated_address, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.UpdateAddressService.update")
    def test_update_address_cannot_get_token_from_request(self, mock_find_address):
        mock_find_address.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.put("/address/update/", self.updated_address, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.UpdateAddressService.update")
    def test_update_address_token_expired_by_replacement(self, mock_update_address):
        mock_update_address.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.put("/address/update/", self.updated_address, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.address_service.UpdateAddressService.update")
    def test_update_address_other_exception(self, mock_update_address):
        mock_update_address.side_effect = DatabaseError("DB connection failed")

        response = self.client.put("/address/update/", self.updated_address, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    def test_update_address_serializer_error(self):
        self.updated_address = {"address": "example_street2", "postal_code": "adsdsf", "city": "London",
                                "country": "UK"}

        response = self.client.put("/address/update/", self.updated_address, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
