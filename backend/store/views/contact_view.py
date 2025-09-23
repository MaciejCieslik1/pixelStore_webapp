from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_username_serializer import CheckUsernameSerializer
from store.serializers.contact_serializer import CreateContactSerializer
from store.serializers.page_serializer import PageSerializer
from store.service.contact_service import FindContactByNameService, FindAllContactsService, CreateContactService, \
    DeleteContactByNameService


class FindContactByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_contact_by_name_service: FindContactByNameService, **kwargs):
        super().__init__(**kwargs)
        self._find_contact_by_name_service = find_contact_by_name_service

    @property
    def find_contact_by_name_service(self):
        return self._find_contact_by_name_service

    def get(self, request: Request, username: str) -> Response:
        serializer = CheckUsernameSerializer(username=username)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                contact_found = self.find_contact_by_name_service.find_by_name(token, request.user, serializer.validated_username)
                return Response(contact_found, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except InvalidInputData as e:
                return Response(
                    {"error": "Invalid input data provided.", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class FindAllContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_contacts_service: FindAllContactsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_contacts_service = find_all_contacts_service

    @property
    def find_all_contacts_service(self):
        return self._find_all_contacts_service

    def get(self, request: Request) -> Response:
        serializer = PageSerializer(data=request.query_params)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                contacts_found = self.find_all_contacts_service.find_all(token, request.user, serializer.validated_data)
                return Response(contacts_found, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except InvalidInputData as e:
                return Response(
                    {"error": "Invalid input data provided.", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateContactView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_contact_service: CreateContactService, **kwargs):
        super().__init__(**kwargs)
        self._create_contact_service = create_contact_service

    @property
    def create_contact_service(self):
        return self._create_contact_service

    def post(self, request: Request) -> Response:
        serializer = CreateContactSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.create_contact_service.create(token, request.user, serializer.validated_data)
                return Response({"msg": communicate}, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except InvalidInputData as e:
                return Response(
                    {"error": "Invalid input data provided.", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteContactByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_contact_by_name_service: DeleteContactByNameService, **kwargs):
        super().__init__(**kwargs)
        self._delete_contact_by_name_service = delete_contact_by_name_service

    @property
    def delete_contact_by_name_service(self):
        return self._delete_contact_by_name_service

    def delete(self, request: Request, username: str) -> Response:
        serializer = CheckUsernameSerializer(username=username)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.delete_contact_by_name_service.delete(token, request.user, serializer.validated_username)
                return Response({"msg": communicate}, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except InvalidInputData as e:
                return Response(
                    {"error": "Invalid input data provided.", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

