from django.db import DatabaseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers.authentication_serializer import RegisterSerializer, LoginSerializer, AccountVerificationSerializer, \
    TokenVerificationSerializer, ResetPasswordSerializer, ResendVerificationCodeSerializer
from ..service.authentication_service import *
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
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                communicate = self.register_service.register_user(serializer.validated_data)
                return Response({"msg": communicate}, status=status.HTTP_201_CREATED)
            except (EmailAlreadyTakenError, UsernameAlreadyTakenError) as e:
                return Response(
                    {"error": "Validation error", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except DatabaseError as e:
                return Response(
                    {"error": "Database error occurred.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def __init__(self, login_service: LoginService, **kwargs):
        super().__init__(**kwargs)
        self._login_service = login_service

    @property
    def login_service(self):
        return self._login_service

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tokens = self.login_service.login_user(serializer.validated_data)
                return Response({
                            "msg": "User successfully logged in.",
                            "access_token": tokens["access_token"],
                            "refresh_token": tokens["refresh_token"],},
                            status=status.HTTP_200_OK
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
            except UserNotVerifiedError as e:
                return Response(
                        {"error": "Validation error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, logout_service: LogoutService, **kwargs):
        super().__init__(**kwargs)
        self._logout_service = logout_service

    @property
    def logout_service(self):
        return self._logout_service

    def post(self, request: Request) -> Response:
        try:
            token = TokenUtils.get_jwt_token_from_request(request)
            communicate = self.logout_service.logout_user(token, request.user)
            return Response({"msg": communicate}, status=status.HTTP_200_OK)
        except (TokenExpiredError, CannotGetTokenFromRequestError) as e:
            return Response(
                {"error": "Access token error.", "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyAccountView(APIView):
    def __init__(self, verify_account_service: VerifyAccountService, **kwargs):
        super().__init__(**kwargs)
        self._verify_account_service = verify_account_service

    @property
    def verify_account_service(self):
        return self._verify_account_service

    def post(self, request: Request) -> Response:
        serializer = AccountVerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                self.verify_account_service.verify_account(serializer.validated_data)
                return Response({"msg": "Account successfully verified."}, status=status.HTTP_200_OK)
            except (InvalidVerificationCodeError, ExpiredVerificationCodeError) as e:
                return Response(
                    {"error": "Verification code error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenView(APIView):
    def __init__(self, verify_token_service: VerifyTokenService, **kwargs):
        super().__init__(**kwargs)
        self._verify_token_service = verify_token_service

    @property
    def verify_token_service(self):
        return self._verify_token_service

    def post(self, request: Request) -> Response:
        serializer = TokenVerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                self.verify_token_service.verify_token(serializer.validated_data)
                return Response({"valid": True, "msg": "Token is valid."}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({'valid': False, 'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({'valid': False, 'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def __init__(self, refresh_token_service: RefreshTokenService, **kwargs):
        super().__init__(**kwargs)
        self._refresh_token_service = refresh_token_service

    @property
    def refresh_token_service(self):
        return self._refresh_token_service

    def post(self, request: Request) -> Response:
        serializer = TokenVerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                access_token = self.refresh_token_service.refresh_access_token(serializer.validated_data)
                return Response({
                    "msg": "Access token successfully refreshed.",
                    "access_token": access_token},
                    status=status.HTTP_200_OK
                )
            except RefreshTokenExpiredError:
                return Response({
                    "msg": "Failed to refresh access token.",
                    'error': 'Refresh token expired.'},
                    status=status.HTTP_401_UNAUTHORIZED)
            except InvalidRefreshTokenError:
                return Response({
                    "msg": "Failed to refresh access token.",
                    'error': 'Invalid refresh token.'},
                    status=status.HTTP_401_UNAUTHORIZED)
            except TokenTypeMismatchError:
                return Response({
                    "msg": "Failed to refresh access token.",
                    'error': 'Access token instead of refresh token provided.'},
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, reset_password_service: ResetPasswordService, **kwargs):
        super().__init__(**kwargs)
        self._reset_password_service = reset_password_service

    @property
    def reset_password_service(self):
        return self._reset_password_service

    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                self.reset_password_service.reset_password(token, serializer.validated_data)
                return Response({"msg": "Password changed successfully."}, status=status.HTTP_200_OK)
            except (InvalidVerificationCodeError, ExpiredVerificationCodeError) as e:
                return Response(
                    {"error": "Verification code error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except PasswordsNotMatchError as e:
                return Response(
                    {"error": "Changing password error.", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except (TokenExpiredError, CannotGetTokenFromRequestError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, resend_verification_code_service: ResendVerificationCodeService, **kwargs):
        super().__init__(**kwargs)
        self._resend_verification_code_service = resend_verification_code_service

    @property
    def resend_verification_code_service(self):
        return self._resend_verification_code_service

    def post(self, request: Request) -> Response:
        serializer = ResendVerificationCodeSerializer(user=request.user)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                self.resend_verification_code_service.resend_verification_code(token, serializer.validated_data)
                return Response({"msg": "Verification code sent."}, status=status.HTTP_200_OK)
            except (InvalidVerificationCodeError, ExpiredVerificationCodeError) as e:
                return Response(
                    {"error": "Verification code error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except (TokenExpiredError, CannotGetTokenFromRequestError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)