from store.helper_classes.authentication_helper import TokenUtils
from store.models import User


class FindAddressService:
    def find(self, token: str, user: User) -> dict:
        TokenUtils.verify_access_token(token, user)
        address_data = {"address": user.address.address, "postal_code": user.address.postal_code, "city": user.address.city,
                        "country": user.address.country}
        return address_data

class UpdateAddressService:
    def update(self, token: str, user: User, new_address_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)
        address = user.address
        address.address = new_address_data["address"]
        address.postal_code = new_address_data["postal_code"]
        address.city = new_address_data["city"]
        address.country = new_address_data["country"]
        address.save()
        return "Address successfully updated."
