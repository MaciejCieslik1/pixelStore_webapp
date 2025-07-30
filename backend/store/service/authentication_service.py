from django.contrib.auth.hashers import make_password

from backend.store.exceptions import EmailAlreadyTakenError, UsernameAlreadyTakenError
from backend.store.models import User, UserPreferences, UserStatistics, Address, VerificationCode


class RegisterService:
    def register_user(self, data: dict) -> str:
        password_hash = make_password(data["password"])

        user = User.create_user(data, password_hash)

        if User.objects.filter(email=data["email"]).exists():
            raise EmailAlreadyTakenError("User with this email already exists.")

        if User.objects.filter(username=data["username"]).exists():
            raise UsernameAlreadyTakenError("User with this username already exists.")

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
