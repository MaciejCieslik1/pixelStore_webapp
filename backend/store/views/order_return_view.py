from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_id_serializer import CheckIdSerializer
from store.serializers.order_return_serializer import CreateOrderReturnSerializer
from store.service.order_return_service import FindByIdOrderReturnService, UpdateOrderReturnService, \
    CreateOrderReturnService


class FindByIdOrderReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_order_return_service: FindByIdOrderReturnService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_order_return_service = find_by_id_order_return_service

    @property
    def find_by_id_order_return_service(self):
        return self._find_by_id_order_return_service

    def get(self, request: Request, order_return_id: int) -> Response:
        serializer = CheckIdSerializer(id=order_return_id, name="Order return")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                order_return_found = self.find_by_id_order_return_service.find_by_id(token, request.user, order_return_id)
                return Response(order_return_found, status=status.HTTP_200_OK)
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


class CreateOrderReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_order_return_service: CreateOrderReturnService, **kwargs):
        super().__init__(**kwargs)
        self._create_order_return_service = create_order_return_service

    @property
    def create_order_return_service(self):
        return self._create_order_return_service

    def post(self, request: Request) -> Response:
        serializer = CreateOrderReturnSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.create_order_return_service.create(token, request.user, serializer.validated_data)
                return Response({"msg": communicate}, status=status.HTTP_200_OK)
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_order_return_service: UpdateOrderReturnService, **kwargs):
        super().__init__(**kwargs)
        self._update_order_return_service = update_order_return_service

    @property
    def update_order_return_service(self):
        return self._update_order_return_service

    def put(self, request: Request, order_return_id: int) -> Response:
        serializer = CheckIdSerializer(id=order_return_id, name="Order return")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.update_order_return_service.update(token, request.user, order_return_id)
                return Response({"msg": communicate}, status=status.HTTP_200_OK)
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
