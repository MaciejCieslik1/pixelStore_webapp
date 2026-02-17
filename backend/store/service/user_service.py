from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User
from store.output_serializers.user_output_serializer import UserOutputSerializer


class FindByUsernameUserService:
    def find_by_username(self, token: str, user: User, username: str) -> dict:
        TokenUtils.verify_access_token(token, user)

        user = User.objects.filter(username=username).first()
        if user is None:
            raise InvalidInputData("User with this username does not exist.")

        serializer = UserOutputSerializer(user)
        return serializer.data


class UpdateUserService:
    def update(self, token : str, user: User, update_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)

        user.money = update_data["money"]
        user.bio = update_data["bio"]

        user.save()

        return "User data updated successfully."


class DeleteAccountUserService:
    def delete(self, token : str, user: User) -> str:
        TokenUtils.verify_access_token(token, user)

        user.delete()

        return "Deleted account successfully."
