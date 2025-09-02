from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, CannotGetTokenFromRequestError, TokenExpiredByReplacementError, \
    TokenExpiredError, UserNotFoundError, NotificationNotFoundError, NotificationNotBelongToUserError
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.notification_serializer import FindAllNotificationsSerializer, CreateNotificationSerializer, \
    DeleteNotificationSerializer
from store.service.notification_service import FindAllNotificationsService, CreateNotificationService, \
    DeleteNotificationService


class FindAllNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_notifications_service: FindAllNotificationsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_notifications_service = find_all_notifications_service

    @property
    def find_all_notifications_service(self):
        return self._find_all_notifications_service

    def get(self, request: Request) -> Response:
        serializer = FindAllNotificationsSerializer(data=request.query_params)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)

                date_from = serializer.validated_data.get("date_from")
                date_to = serializer.validated_data.get("date_to")
                order = serializer.validated_data.get("order", "desc")
                page = serializer.validated_data.get("page", 1)
                page_size = serializer.validated_data.get("page_size", 10)

                notifications_found = self.find_all_notifications_service.find_all(token, serializer.validated_data,
                    date_from, date_to, order, page, page_size)
                return Response(notifications_found, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_notification_service: CreateNotificationService, **kwargs):
        super().__init__(**kwargs)
        self._create_notification_service = create_notification_service

    @property
    def create_notification_service(self):
        return self._create_notification_service

    def post(self, request: Request) -> Response:
        serializer = CreateNotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                self.create_notification_service.create(token, request.user, serializer.validated_data)
                return Response({"msg": "Notification created successfully."}, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except UserNotFoundError as e:
                return Response(
                    {"error": "User not found.", "details": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_notification_service: DeleteNotificationService, **kwargs):
        super().__init__(**kwargs)
        self._delete_notification_service = delete_notification_service

    @property
    def delete_notification_service(self):
        return self._delete_notification_service

    def delete(self, request: Request) -> Response:
        serializer = DeleteNotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                self.delete_notification_service.delete(token, request.user, serializer.validated_data)
                return Response({"msg": "Notification deleted successfully."}, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except NotificationNotFoundError as e:
                return Response(
                    {"error": "Notification not found.", "details": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )
            except NotificationNotBelongToUserError as e:
                return Response(
                    {"error": "Notification does not belong to the user.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
