from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_id_serializer import CheckIdSerializer
from store.serializers.page_serializer import PageSerializer
from store.serializers.transaction_serializer import CreateTransactionSerializer
from store.service.transaction_service import FindByIdTransactionService, FindAllMineTransactionsService, \
    CreateTransactionService, UpdateTransactionService


class FindByIdTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_transaction_service: FindByIdTransactionService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_transaction_service = find_by_id_transaction_service

    @property
    def find_by_id_transaction_service(self):
        return self._find_by_id_transaction_service

    def get(self, request: Request, transaction_id: int) -> Response:
        serializer = CheckIdSerializer(id=transaction_id, name="Transaction")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                product_review_found = self.find_by_id_transaction_service.find_by_id(token, request.user, transaction_id)
                return Response(product_review_found, status=status.HTTP_200_OK)
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


class FindAllMineTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_mine_transactions_service: FindAllMineTransactionsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_mine_transactions_service = find_all_mine_transactions_service

    @property
    def find_all_mine_transactions_service(self):
        return self._find_all_mine_transactions_service

    def get(self, request: Request) -> Response:
        serializer = PageSerializer(data=request.query_params)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                products_found = self.find_all_mine_transactions_service.find_all_mine(token, request.user,
                                                                                        serializer.validated_data)
                return Response(products_found, status=status.HTTP_200_OK)
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


class CreateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_transaction_service: CreateTransactionService, **kwargs):
        super().__init__(**kwargs)
        self._create_transaction_service = create_transaction_service

    @property
    def create_transaction_service(self):
        return self._create_transaction_service

    def post(self, request: Request) -> Response:
        serializer = CreateTransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                result_data = self.create_transaction_service.create(token, request.user, serializer.validated_data)
                return Response(result_data, status=status.HTTP_201_CREATED)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except InvalidInputData as e:
                return Response(
                    {"error": "Invalid input data provided.", "details": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_transaction_service: UpdateTransactionService, **kwargs):
        super().__init__(**kwargs)
        self._update_transaction_service = update_transaction_service

    @property
    def update_transaction_service(self):
        return self._update_transaction_service

    def put(self, request: Request, transaction_id: int) -> Response:
        serializer = CheckIdSerializer(id=transaction_id, name="Transaction")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.update_transaction_service.update(token, request.user, transaction_id)
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
