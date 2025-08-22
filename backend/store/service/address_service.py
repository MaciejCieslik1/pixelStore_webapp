from store.models import User


class FindAddressService:
    def find(self, token: str, user: User):
        pass


class UpdateAddressService:
    def update(self, token: str, user: User, new_address_data: dict):
        pass