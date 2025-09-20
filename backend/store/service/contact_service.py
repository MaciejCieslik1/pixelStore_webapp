from store.models import User

class FindContactByNameService:
    def find_by_name(self, token: str, user: User, username: str) -> dict:
        pass


class FindAllContactsService:
    def find_all(self, token: str, user: User) -> list:
        pass


class CreateContactService:
    def create(self, token: str, user: User, new_contact_data: dict) -> str:
        pass


class DeleteContactByNameService:
    def delete(self, token: str, user: User, username: str) -> str:
        pass
