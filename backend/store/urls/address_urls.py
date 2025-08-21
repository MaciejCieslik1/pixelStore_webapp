from django.urls import path
from store.views.address_view import *

find_address_service = FindAddressService()
update_address_service = UpdateAddressService()

urlpatterns = [
    path("find/", FindAddressView.as_view(find_address_service=find_address_service), name="find_address"),
    path("update/", UpdateAddressView.as_view(update_address_service=update_address_service), name="update_address"),
]