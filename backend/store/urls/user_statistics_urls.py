from django.urls import path

from store.service.user_statistics_service import FindByUsernameUserStatisticsService
from store.views.user_statistics_view import FindByUsernameUserStatisticsView

find_by_username_user_statistics_service = FindByUsernameUserStatisticsService()

urlpatterns = [
    path("find_by_username/<str:username>/", FindByUsernameUserStatisticsView.as_view(
        find_by_username_user_statistics_service=find_by_username_user_statistics_service), name="find_by_username/<str:username>"),
]
