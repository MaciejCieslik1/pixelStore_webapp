from django.urls import path

from store.service.user_preferences_service import FindUserPreferencesService, UpdateUserPreferencesService
from store.views.user_preferences_view import FindUserPreferencesView, UpdateUserPreferencesView

find_user_preferences_service = FindUserPreferencesService()
update_service = UpdateUserPreferencesService()

urlpatterns = [
    path("find/", FindUserPreferencesView.as_view(
        find_user_preferences_service=find_user_preferences_service), name="find"),
    path("update/", UpdateUserPreferencesView.as_view(update_user_preferences_service=update_service),
         name="update_user_preferences"),
]
