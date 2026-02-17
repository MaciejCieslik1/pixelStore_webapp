from django.urls import path

from store.service.user_service import FindByUsernameUserService, UpdateUserService, DeleteAccountUserService
from store.views.user_view import FindByUsernameUserView, UpdateUserView, DeleteAccountUserView

find_by_username_user_service = FindByUsernameUserService()
update_service = UpdateUserService()
delete_account_user_service = DeleteAccountUserService()

urlpatterns = [
    path("find_by_username/<str:username>/", FindByUsernameUserView.as_view(
        find_by_username_user_service=find_by_username_user_service), name="find_by_username/<str:username>"),
    path("update/", UpdateUserView.as_view(update_user_service=update_service), name="update_user"),
    path("delete_account/", DeleteAccountUserView.as_view(delete_account_user_service=delete_account_user_service),
         name="delete_account")
]
