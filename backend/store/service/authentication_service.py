import uuid
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from ..models import User, UserPreferences, UserStatistics, Address, VerificationCode
from ..exceptions import *
import jwt

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'


class RegisterService:
    def register_user(self, data: dict) -> str:
        self.check_if_email_or_username_occupied(data)

        user = User.create_user(data)
        user_preferences = UserPreferences.create_user_preferences(user)
        user_statistics = UserStatistics.create_user_statistics(user)
        address = Address.create_address(data, user)
        verification_code = VerificationCode.create_verification_code(user)

        with transaction.atomic():
            user.save()
            user_preferences.save()
            user_statistics.save()
            address.save()
            verification_code.save()

        EmailService.send_code(data["email"], verification_code)

        return f"User {user.username} registered successfully"

    def check_if_email_or_username_occupied(self, data: dict):
        if User.objects.filter(email=data["email"]).exists():
            raise EmailAlreadyTakenError("User with this email already exists.")
        if User.objects.filter(username=data["username"]).exists():
            raise UsernameAlreadyTakenError("User with this username already exists.")


class EmailService:
    @staticmethod
    def send_code(email: str, verification_code: str):
        subject = "Verification code to pixelStore"
        message = f"Hi. This is you verification code: {verification_code}"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email], fail_silently=False)


class LoginService:
    def login_user(self, data: dict) -> dict:
        user = self.verify_user(data)
        return {
            'access_token': TokenGenerator.generate_access_token(user),
            'refresh_token': TokenGenerator.generate_refresh_token(user)
        }

    def verify_user(self, data: dict) -> User:
        email = data.get('email')
        password = data.get('password')

        self.check_if_email_and_username_are_not_empty(email, password)
        user = self.find_user_if_exists(email)
        self.check_password_correctness(password, user.password) # user.password is hashed password

        if user.is_verified is False:
            raise UserNotVerifiedError("User not verified.")

        return user

    def check_if_email_and_username_are_not_empty(self, email: str, password: str):
        if email is None:
            raise MissingEmailError("Email is missing.")
        if password is None:
            raise MissingPasswordError("Password is missing.")

    def find_user_if_exists(self, email: str) -> User:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserNotFoundError("User with provided email not found.")

    def check_password_correctness(self, password: str, password_hash: str):
        if not check_password(password, password_hash):
            raise InvalidPasswordError("Invalid password.")


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


class LogoutService:
    def logout_user(self) -> str:
        return "User successfully logged out."


class VerifyAccountService:
    def verify_account(self, data: dict):
        try:
            user = User.objects.get(email=data["email"])
        except ObjectDoesNotExist:
            raise UserNotFoundError("User with provided email does not exist.")

        VerificationCodeHandling.check_verification_code_credentials(user, data["code"])

        user.is_verified = True
        user.save()

        VerificationCodeHandling.change_verification_code(user)


class VerificationCodeHandling:
    @staticmethod
    def check_verification_code_credentials(user: User, input_code: str):
        if not hasattr(user, 'verification_code'):
            raise NoVerificationCodeFoundError("No verification code found.")
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
        EmailService.send_code(user.email, verification_code)


class VerifyTokenService:
    def verify_token(self, data: dict):
        token = data.get('token')
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


class RefreshTokenService:
    def refresh_access_token(self, data: dict) -> str:
        user_id = self.get_user_id_from_refresh_token(data)
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise UserNotFoundError("User with provided id not found.")
        return TokenGenerator.generate_access_token(user)

    def get_user_id_from_refresh_token(self, data: dict) -> int:
        refresh_token = data.get('refresh_token')
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('user_id')


class ResetPasswordService:
    def reset_password(self, user: User, data: dict):
        if data["code"] != user.verification_code.code:
            raise InvalidVerificationCodeError("Incorrect verification code.")

        if data["password1"] != data["password2"]:
            raise PasswordsNotMatchError("Passwords don't match.")

        password_hash = make_password(data["password1"])
        user.password = password_hash
        user.save()


class ResendVerificationCodeService:
    def resend_verification_code(self, user: User):
        VerificationCodeHandling.change_verification_code(user)
