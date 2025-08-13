from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from jwt import ExpiredSignatureError

from ..exceptions import *
from ..models import User, VerificationCode
import uuid
import jwt

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'


class VerificationCodeHandling:
    @staticmethod
    def check_verification_code_credentials(user: User, input_code: str):
        if user.verification_code.code != input_code:
            raise InvalidVerificationCodeError("Incorrect verification code.")
        if user.verification_code.expiration_date_time < timezone.now():
            VerificationCodeHandling.change_verification_code(user)
            raise ExpiredVerificationCodeError("Verification code has expired.")

    @staticmethod
    def change_verification_code(user: User):
        verification_code = user.verification_code
        verification_code.delete()
        verification_code = VerificationCode.create_verification_code(user)
        verification_code.save()
        EmailSender.send_code(user.email, verification_code)


class TokenGenerator:
    @staticmethod
    def generate_access_token(user: User) -> str:
        now = timezone.now()
        access_payload = {
            'user_id': user.user_id,
            'token_type': 'access',
            'jti': str(uuid.uuid4()),
            'exp': now + timedelta(minutes=15),
            'iat': now,
            'token_version': user.token_version,
        }
        return jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def generate_refresh_token(user: User) -> str:
        now = timezone.now()
        refresh_payload = {
            'user_id': user.user_id,
            'token_type': 'refresh',
            'jti': str(uuid.uuid4()),
            'exp': now + timedelta(days=1),
            'iat': now,
        }
        return jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)


class EmailSender:
    @staticmethod
    def send_code(email: str, verification_code: str):
        subject = "Verification code to pixelStore"
        message = f"Hi. This is you verification code: {verification_code}"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email], fail_silently=False)


class TokenUtils:
    @staticmethod
    def verify_access_token(token: str, user: User):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
            raise TokenExpiredError("Access token has expired.")
        except InvalidTokenError:
            raise IncorrectTokenError("Incorrect access token.")
        if payload.get('token_version') != user.token_version:
            raise TokenExpiredByReplacementError("Access token is no longer valid.")

    @staticmethod
    def get_jwt_token_from_request(request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            return auth_header[len('Bearer '):]
        raise CannotGetTokenFromRequestError("Cannot get token from http request.")
