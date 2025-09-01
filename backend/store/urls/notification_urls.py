from django.urls import path
from store.views.notification_view import *


find_all_notifications_service = FindAllNotificationsService()
create_service = CreateNotificationService()
delete_service = DeleteNotificationService()

urlpatterns = [
    path("find_all/", FindAllNotificationsView.as_view(find_all_notifications_service=find_all_notifications_service),
         name="find_all_notifications"),
    path("create/", CreateNotificationView.as_view(create_notification_service=create_service),
         name="create_notification"),
    path("delete/", DeleteNotificationView.as_view(delete_notification_service=delete_service),
         name="delete_notification"),
]
