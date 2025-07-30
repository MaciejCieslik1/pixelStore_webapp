from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from backend.config.settings import SECRET_KEY
from backend.store.models import User, UserPreferences, UserStatistics, Address, VerificationCode
from backend.store.views.authentication_view import ALGORITHM
from backend.store.exceptions import EmailAlreadyTakenError, UsernameAlreadyTakenError, MissingEmailError, \
    MissingPasswordError, UserNotFoundError, InvalidPasswordError
import jwt


class RegisterService:
    def register_user(self, data: dict) -> str:
        self.check_if_email_or_username_occupied(data)
        password_hash = make_password(data["password"])
        user = User.create_user(data, password_hash)

        user.save()

        user_preferences = UserPreferences.create_user_preferences(user)
        user_preferences.save()

        user_statistics = UserStatistics.create_user_statistics(user)
        user_statistics.save()

        address = Address.create_address(data, user)
        address.save()

        verification_code = VerificationCode.create_verification_code(user)
        verification_code.save()

        return f"User {user.username} registered successfully"

    def check_if_email_or_username_occupied(self, data: dict):
        if User.objects.filter(email=data["email"]).exists():
            raise EmailAlreadyTakenError("User with this email already exists.")
        if User.objects.filter(username=data["username"]).exists():
            raise UsernameAlreadyTakenError("User with this username already exists.")


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
        self.check_password_correctness(password, user.password_hash)

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
            'exp': now + timedelta(minutes=15),
            'iat': now,
        }
        return jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def generate_refresh_token(user: User) -> str:
        now = timezone.now()
        refresh_payload = {
            'user_id': user.user_id,
            'exp': now + timedelta(days=1),
            'iat': now,
        }
        return jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)


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
        return  TokenGenerator.generate_access_token(user)

    def get_user_id_from_refresh_token(self, data: dict) -> int:
        refresh_token = data.get('refresh')
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('user_id')
