from django.urls import path

from store.service.contact_service import FindContactByNameService, FindAllContactsService, CreateContactService, \
    DeleteContactByNameService
from store.views.contact_view import FindContactByNameView, FindAllContactsView, CreateContactView, \
    DeleteContactByNameView

find_contact_by_name_service = FindContactByNameService()
find_all_contacts_service = FindAllContactsService()
create_contact_service = CreateContactService()
delete_contact_by_name_service = DeleteContactByNameService()

urlpatterns = [
    path("find_by_username/<str:username>/", FindContactByNameView.as_view(find_contact_by_name_service=find_contact_by_name_service),
         name="contact_find_by_username"),
    path("find_all/", FindAllContactsView.as_view(find_all_contacts_service=find_all_contacts_service),
         name="contact_find_all"),
    path("create/", CreateContactView.as_view(create_contact_service=create_contact_service),
         name="contact_create"),
    path("delete_by_username/<str:username>/", DeleteContactByNameView.as_view(delete_contact_by_name_service=delete_contact_by_name_service),
         name="contact_delete_by_username"),
]