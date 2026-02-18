from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.update_user_preferences_serializer import UpdateUserPreferencesSerializer
from store.service.user_preferences_service import FindUserPreferencesService, UpdateUserPreferencesService


class FindUserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_user_preferences_service: FindUserPreferencesService, **kwargs):
        super().__init__(**kwargs)
        self._find_user_preferences_service = find_user_preferences_service

    @property
    def find_user_preferences_service(self):
        return self._find_user_preferences_service

    def get(self, request: Request) -> Response:
        try:
            token = TokenUtils.get_jwt_token_from_request(request)
            user_found = self.find_user_preferences_service.find(token, request.user)
            return Response(user_found, status=status.HTTP_200_OK)
        except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                TokenExpiredByReplacementError) as e:
            return Response(
                {"error": "Access token error.", "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateUserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_user_preferences_service: UpdateUserPreferencesService, **kwargs):
        super().__init__(**kwargs)
        self._update_user_preferences_service = update_user_preferences_service

    @property
    def update_user_preferences_service(self):
        return self._update_user_preferences_service

    def put(self, request: Request) -> Response:
        serializer = UpdateUserPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.update_user_preferences_service.update(token, request.user, serializer.validated_data)
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
