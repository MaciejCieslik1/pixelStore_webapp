from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import TokenExpiredByReplacementError, CannotGetTokenFromRequestError, TokenExpiredError, \
    IncorrectTokenError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user, AuthenticationHelper
from store.helper_tests_classes.contact_test_helper import ContactTestHelper
from store.models import User


@pytest.mark.django_db
class TestFindByUsernameContact:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.contact = ContactTestHelper.create_contact(self.user)
        self.receiver_username = self.contact.receiver.username

    @patch("store.service.contact_service.FindContactByNameService.find_by_name")
    def test_find_by_username_success(self, mock_find_by_name):
        mock_find_by_name.return_value = {"contact_id": self.contact.contact_id, "sender_username": self.contact.sender.username,
             "receiver_username": self.receiver_username}

        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["contact_id"] == self.contact.contact_id
        assert response.data["sender_username"] == self.contact.sender.username
        assert response.data["receiver_username"] == self.receiver_username
        mock_find_by_name.assert_called_once()

    @patch("store.service.contact_service.FindContactByNameService.find_by_name")
    def test_find_by_username_invalid_token(self, mock_find_by_name):
        mock_find_by_name.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindContactByNameService.find_by_name")
    def test_find_by_username_expired_token(self, mock_find_by_name):
        mock_find_by_name.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindContactByNameService.find_by_name")
    def test_find_by_username_cannot_get_token_from_request(self, mock_find_by_name):
        mock_find_by_name.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindContactByNameService.find_by_name")
    def test_find_by_username_token_expired_by_replacement(self, mock_find_by_name):
        mock_find_by_name.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindContactByNameService.find_by_name")
    def test_find_by_username_other_exception(self, mock_find_by_name):
        mock_find_by_name.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.contact_service.FindContactByNameService.find_by_name")
    def test_find_by_username_invalid_input_data(self, mock_find_by_name):
        mock_find_by_name.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_by_username_invalid_serializer(self):
        self.receiver_username = ""
        response = self.client.get(f"/contact/find_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestFindAllContacts:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.contact = ContactTestHelper.create_contact(self.user)
        self.receiver_username = self.contact.receiver.username

    @patch("store.service.contact_service.FindAllContactsService.find_all")
    def test_find_all_success(self, mock_find_all):
        mock_find_all.return_value = [
            {"contact_id": self.contact.contact_id, "sender_username": self.contact.sender.username,
                "receiver_username": self.receiver_username},
            {"contact_id": self.contact.contact_id + 1, "sender_username": self.contact.sender.username,
                "receiver_username": "example_username"}]
        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["contact_id"] == self.contact.contact_id
        assert response.data[0]["sender_username"] == self.contact.sender.username
        assert response.data[0]["receiver_username"] == self.receiver_username
        mock_find_all.assert_called_once()

    @patch("store.service.contact_service.FindAllContactsService.find_all")
    def test_find_all_invalid_token(self, mock_find_all):
        mock_find_all.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindAllContactsService.find_all")
    def test_find_all_expired_token(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindAllContactsService.find_all")
    def test_find_all_cannot_get_token_from_request(self, mock_find_all):
        mock_find_all.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindAllContactsService.find_all")
    def test_find_all_token_expired_by_replacement(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.FindAllContactsService.find_all")
    def test_find_all_other_exception(self, mock_find_all):
        mock_find_all.side_effect = DatabaseError("DB connection failed")

        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.contact_service.FindAllContactsService.find_all")
    def test_find_all_invalid_input_data(self, mock_find_all):
        mock_find_all.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_find_all_invalid_serializer(self):
        self.receiver_username = ""
        response = self.client.get("/contact/find_all/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCreateOrderProduct:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        user2_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                      "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                      "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                      "country": "Poland"}
        AuthenticationHelper.register_and_login_user(user2_data)
        self.user2 = User.objects.get(username=user2_data["username"])
        self.data = {"receiver_username": self.user2.username}

    @patch("store.service.contact_service.CreateContactService.create")
    def test_create_success(self, mock_create):
        mock_create.return_value = "Contact created successfully."

        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Contact created successfully."
        mock_create.assert_called_once()

    @patch("store.service.contact_service.CreateContactService.create")
    def test_create_invalid_token(self, mock_create):
        mock_create.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.CreateContactService.create")
    def test_create_expired_token(self, mock_create):
        mock_create.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.CreateContactService.create")
    def test_create_cannot_get_token_from_request(self, mock_create):
        mock_create.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.CreateContactService.create")
    def test_create_token_expired_by_replacement(self, mock_create):
        mock_create.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.CreateContactService.create")
    def test_create_other_exception(self, mock_create):
        mock_create.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.contact_service.CreateContactService.create")
    def test_create_invalid_input_data(self, mock_create):
        mock_create.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_create_invalid_serializer(self):
        self.data = {}
        response = self.client.post("/contact/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteContactByUsername:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.contact = ContactTestHelper.create_contact(self.user)
        self.receiver_username = self.contact.receiver.username

    @patch("store.service.contact_service.DeleteContactByNameService.delete")
    def test_delete_success(self, mock_delete):
        mock_delete.return_value = "Contact deleted successfully."

        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Contact deleted successfully."
        mock_delete.assert_called_once()

    @patch("store.service.contact_service.DeleteContactByNameService.delete")
    def test_delete_invalid_token(self, mock_delete):
        mock_delete.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.DeleteContactByNameService.delete")
    def test_delete_expired_token(self, mock_delete):
        mock_delete.side_effect = TokenExpiredError("Access token error.")

        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.DeleteContactByNameService.delete")
    def test_delete_cannot_get_token_from_request(self, mock_delete):
        mock_delete.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.DeleteContactByNameService.delete")
    def test_delete_token_expired_by_replacement(self, mock_delete):
        mock_delete.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.contact_service.DeleteContactByNameService.delete")
    def test_delete_other_exception(self, mock_delete):
        mock_delete.side_effect = DatabaseError("DB connection failed")

        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.contact_service.DeleteContactByNameService.delete")
    def test_delete_invalid_input_data(self, mock_delete):
        mock_delete.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_delete_invalid_serializer(self):
        self.receiver_username = "a" * 33
        response = self.client.delete(f"/contact/delete_by_username/{self.receiver_username}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
