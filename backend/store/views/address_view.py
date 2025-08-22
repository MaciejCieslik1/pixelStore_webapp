from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.address_serializer import UpdateAddressSerializer
from store.service.address_service import FindAddressService, UpdateAddressService


class FindAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_address_service: FindAddressService, **kwargs):
        super().__init__(**kwargs)
        self._find_address_service = find_address_service

    @property
    def find_address_service(self):
        return self._find_address_service

    def get(self, request: Request) -> Response:
        try:
            token = TokenUtils.get_jwt_token_from_request(request)
            address_found = self.find_address_service.find(token, request.user)
            return Response(address_found, status=status.HTTP_200_OK)
        except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, TokenExpiredByReplacementError) as e:
            return Response(
                {"error": "Access token error.", "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_address_service: UpdateAddressService, **kwargs):
        super().__init__(**kwargs)
        self._update_address_service = update_address_service

    @property
    def update_address_service(self):
        return self._update_address_service

    def put(self, request: Request) -> Response:
        serializer = UpdateAddressSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                self.update_address_service.update(token, request.user, serializer.validated_data)
                return Response({"msg": "Address successfully updated."}, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)