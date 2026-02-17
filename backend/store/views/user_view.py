from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_username_serializer import CheckUsernameSerializer
from store.serializers.user_serializer import UpdateUserSerializer
from store.service.user_service import FindByUsernameUserService, UpdateUserService, DeleteAccountUserService


class FindByUsernameUserView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_username_user_service: FindByUsernameUserService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_username_user_service = find_by_username_user_service

    @property
    def find_by_username_user_service(self):
        return self._find_by_username_user_service

    def get(self, request: Request, username: str) -> Response:
        serializer = CheckUsernameSerializer(username=username)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                user_found = self.find_by_username_user_service.find_by_username(token, request.user, username)
                return Response(user_found, status=status.HTTP_200_OK)
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


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_user_service: UpdateUserService, **kwargs):
        super().__init__(**kwargs)
        self._update_user_service = update_user_service

    @property
    def update_user_service(self):
        return self._update_user_service

    def put(self, request: Request) -> Response:
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.update_user_service.update(token, request.user, serializer.validated_data)
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


class DeleteAccountUserView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_account_user_service: DeleteAccountUserService, **kwargs):
        super().__init__(**kwargs)
        self._delete_account_user_service = delete_account_user_service

    @property
    def delete_account_user_service(self):
        return self._delete_account_user_service

    def delete(self, request: Request) -> Response:
        try:
            token = TokenUtils.get_jwt_token_from_request(request)
            communicate = self.delete_account_user_service.delete(token, request.user)
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
