from django.db import DatabaseError
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.conf import settings
from backend.store.exceptions import EmailAlreadyTakenError, UsernameAlreadyTakenError, MissingEmailError, \
    MissingPasswordError, InvalidPasswordError, UserNotFoundError
from backend.store.service.authentication_service import RegisterService, LoginService, VerifyTokenService
import jwt


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'


class RegisterView(APIView):
    def __init__(self, register_service: RegisterService, **kwargs):
        super().__init__(**kwargs)
        self._register_service = register_service

    @property
    def register_service(self):
        return self._register_service

    def post(self, request: Request) -> Response:
        try:
            communicate = self.register_service.register_user(request.data)
            return Response({"msg": communicate}, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response(
                {"error": f"Missing field: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except (EmailAlreadyTakenError, UsernameAlreadyTakenError) as e:
            return Response(
                {"error": "Validation error", "details": e.message_dict if hasattr(e, "message_dict") else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DatabaseError:
            return Response(
                {"error": "Database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    def __init__(self, login_service: LoginService, **kwargs):
        super().__init__(**kwargs)
        self._login_service = login_service

    @property
    def login_service(self):
        return self._login_service

    def post(self, request: Request) -> Response:
        try:
            access_token, refresh_token = self.login_service.login_user(request.data)
            return Response({
                        "msg": "User successfully logged.",
                        "access_token": access_token,
                        "refresh_token": refresh_token},
                        status=status.HTTP_200_OK
            )
        except (MissingEmailError, MissingPasswordError) as e:
            return Response(
                {"error": "Missing credentials.", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except UserNotFoundError as e:
            return Response(
                {"error": "User not found.", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidPasswordError as e:
            return Response(
                {"error": "Invalid credentials.", "details": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyTokenView(APIView):
    def __init__(self, verify_token_service: VerifyTokenService, **kwargs):
        super().__init__(**kwargs)
        self._verify_token_service = verify_token_service

    @property
    def verify_token_service(self):
        return self._verify_token_service

    def post(self, request):
        try:
            self.verify_token_service.verify_token(request.data)
            return Response({"valid": True, "msg": "Access token is valid."}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'valid': False, 'error': 'Access token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'valid': False, 'error': 'Invalid access token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {"error": "Unexpected error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshTokenView(APIView):
    def __init__(self, refresh_token_service: RefreshTokenService, **kwargs):
        super().__init__(**kwargs)
        self._refresh_token_service = refresh_token_service

    @property
    def refresh_token_service(self):
        return self._refresh_token_service

    def post(self, request):
        try:
            access_token = self.refresh_token_service.refresh_access_token(request.data)
            return Response({
                "msg": "Access successfully refreshed.",
                "access_token": access_token},
                status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return Response({
                "msg": "Failed to refresh access token.",
                'error': 'Refresh token expired.'},
                status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({
                "msg": "Failed to refresh access token.",
                'error': 'Invalid refresh token.'},
                status=status.HTTP_401_UNAUTHORIZED)
        except UserNotFoundError as e:
            return Response(
                {"error": "User not found.", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
