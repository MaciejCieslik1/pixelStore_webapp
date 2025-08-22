from store.models import Address, User


class AddressTestHelper:
    @staticmethod
    def create_address(user: User):
        address_data = {"address": "example_street", "postal_code": "00001", "city": "Warsaw",
                             "country": "Poland"}
        address = Address.create_address(address_data, user)
        address.save()