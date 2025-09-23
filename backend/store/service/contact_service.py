from django.core.paginator import Paginator
from django.db.models import Q
from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, Contact
from store.output_serializers.contact_output_serializer import ContactOutputSerializer


class FindContactByNameService:
    def find_by_name(self, token: str, user: User, username: str) -> dict:
        TokenUtils.verify_access_token(token, user)

        if user.username == username:
            raise InvalidInputData("Self username provided.")
        contact_user = User.objects.filter(username=username).first()
        if not contact_user:
            raise InvalidInputData("User with that username does not exist.")

        contact = Contact.objects.filter(Q(sender=user, receiver=contact_user) | Q(sender=contact_user, receiver=user)).first()
        if not contact:
            raise InvalidInputData("User with that username is not your contact.")

        serializer = ContactOutputSerializer(contact)
        return serializer.data


class FindAllContactsService:
    def find_all(self, token: str, user: User, validated_data: dict) -> list:
        TokenUtils.verify_access_token(token, user)
        page = validated_data["page"]
        page_size = validated_data["page_size"]

        contacts = Contact.objects.filter(Q(sender=user) | Q(receiver=user)).order_by("-contact_id")

        paginator = Paginator(contacts, page_size)
        page_obj = paginator.get_page(page)

        return [ContactOutputSerializer(contact).data for contact in page_obj]


class CreateContactService:
    def create(self, token: str, user: User, new_contact_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)
        receiver_username = new_contact_data["receiver_username"]

        if receiver_username == user.username:
            raise InvalidInputData("Self username provided.")
        contact_user = User.objects.filter(username=receiver_username).first()
        if not contact_user:
            raise InvalidInputData("User with that username does not exist.")

        contact = Contact.objects.filter(Q(sender=user, receiver=contact_user) | Q(sender=contact_user, receiver=user)).first()
        if contact:
           raise InvalidInputData("User with that username is already your contact.")

        contact = Contact(sender=user, receiver=contact_user)
        contact.save()

        return "Contact created successfully."

class DeleteContactByNameService:
    def delete(self, token: str, user: User, username: str) -> str:
        TokenUtils.verify_access_token(token, user)

        if user.username == username:
            raise InvalidInputData("Self username provided.")
        contact_user = User.objects.filter(username=username).first()
        if not contact_user:
            raise InvalidInputData("User with that username does not exist.")

        contact = Contact.objects.filter(
            Q(sender=user, receiver=contact_user) | Q(sender=contact_user, receiver=user)).first()
        if not contact:
            raise InvalidInputData("User with that username is not your contact.")
        contact.delete()

        return "Contact deleted successfully."
