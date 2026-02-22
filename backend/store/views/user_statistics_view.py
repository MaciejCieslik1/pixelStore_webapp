from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_username_serializer import CheckUsernameSerializer
from store.service.user_statistics_service import FindByUsernameUserStatisticsService


class FindByUsernameUserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_username_user_statistics_service: FindByUsernameUserStatisticsService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_username_user_statistics_service = find_by_username_user_statistics_service

    @property
    def find_by_username_user_statistics_service(self):
        return self._find_by_username_user_statistics_service

    def get(self, request: Request, username: str) -> Response:
        serializer = CheckUsernameSerializer(username=username)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                user_found = self.find_by_username_user_statistics_service.find_by_username(token, request.user, username)
                return Response(user_found, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except InvalidInputData as e:
                return Response(
                    {"error": "Invalid input data provided.", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
