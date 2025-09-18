from django.core.paginator import Paginator
from django.utils import timezone

from store.exceptions import NotificationIdDoesNotBelongToUserError, SelfUsernameError, InvalidUsernameError, \
    InvalidNotificationIdError
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, Notification
from store.output_serializers.notification_output_serializer import NotificationOutputSerializer


class FindAllNotificationsService:
    def find_all(self, token: str, user: User, validated_data: dict):
        TokenUtils.verify_access_token(token, user)
        date_from = validated_data.get("date_from")
        date_to = validated_data.get("date_to")
        order = validated_data.get("order")
        page = validated_data.get("page")
        page_size = validated_data.get("page_size")

        notifications = Notification.objects.filter(receiver=user)

        if date_from:
            notifications = notifications.filter(sent_date_time__gte=date_from)
        if date_to:
            notifications = notifications.filter(sent_date_time__lte=date_to)

        if order == "desc":
            notifications = notifications.order_by("-sent_date_time", "notification_id")
        else:
            notifications = notifications.order_by("sent_date_time", "notification_id")

        response = [NotificationOutputSerializer(notification).data for notification in notifications]

        paginator = Paginator(response, page_size)
        page_obj = paginator.get_page(page)

        return page_obj.object_list


class CreateNotificationService:
    def create(self, token: str, user: User, validated_data: dict):
        TokenUtils.verify_access_token(token, user)
        username = validated_data.get("username")

        if user.username == username:
            raise SelfUsernameError("Self username provided.")

        user_with_username = User.objects.filter(username=username)
        if not user_with_username:
            raise InvalidUsernameError("Invalid username of a notification receiver.")

        receiver = User.objects.get(username=username)
        notification = Notification.objects.create(sender=user, receiver=receiver, sent_date_time=timezone.now(),
            text=validated_data["text"])
        notification.save()
        return "Notification created successfully."


class DeleteNotificationService:
    def delete(self, token: str, user: User, validated_data: dict):
        TokenUtils.verify_access_token(token, user)
        notification = Notification.objects.filter(notification_id=validated_data.get("notification_id")).first()

        if not notification:
            raise InvalidNotificationIdError("Invalid notification id.")

        if notification.sender.user_id != user.user_id and notification.receiver.user_id != user.user_id:
            raise NotificationIdDoesNotBelongToUserError("Notification with given id does not belong to the user.")

        notification.delete()
        return "Notification deleted successfully."
