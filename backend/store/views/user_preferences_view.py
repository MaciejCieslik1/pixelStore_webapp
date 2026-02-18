from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.user_preferences_service import FindUserPreferencesService, UpdateUserPreferencesService


class FindUserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_user_preferences_service: FindUserPreferencesService, **kwargs):
        super().__init__(**kwargs)
        self._find_user_preferences_service = find_user_preferences_service

    @property
    def find_user_preferences_service(self):
        return self._find_user_preferences_service

    def get(self, request: Request) -> Response:
        pass


class UpdateUserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_user_preferences_service: UpdateUserPreferencesService, **kwargs):
        super().__init__(**kwargs)
        self._update_user_preferences_service = update_user_preferences_service

    @property
    def update_user_preferences_service(self):
        return self._update_user_preferences_service

    def put(self, request: Request) -> Response:
        pass
