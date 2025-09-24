from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, CannotGetTokenFromRequestError, TokenExpiredError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_id_serializer import CheckIdSerializer
from store.serializers.product_serializer import FindAllProductsSerializer, CreateProductSerializer
from store.service.product_service import FindByIdProductService, FindAllProductsService, CreateProductService, \
    UpdateProductService, DeleteProductService


class FindByIdProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_product_service: FindByIdProductService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_product_service = find_by_id_product_service

    @property
    def find_by_id_product_service(self):
        return self._find_by_id_product_service

    def get(self, request: Request, product_id: int) -> Response:
        serializer = CheckIdSerializer(id=product_id, name="Product")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                product_found = self.find_by_id_product_service.find_by_id(token, request.user, product_id)
                return Response(product_found, status=status.HTTP_200_OK)
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


class FindAllProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_products_service: FindAllProductsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_products_service = find_all_products_service

    @property
    def find_all_products_service(self):
        return self._find_all_products_service

    def get(self, request: Request) -> Response:
        serializer = FindAllProductsSerializer(data=request.query_params)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                products_found = self.find_all_products_service.find_all(token, request.user, serializer.validated_data)
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


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_product_service: CreateProductService, **kwargs):
        super().__init__(**kwargs)
        self._create_product_service = create_product_service

    @property
    def create_product_service(self):
        return self._create_product_service

    def post(self, request: Request) -> Response:
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.create_product_service.create(token, request.user, serializer.validated_data)
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
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, update_product_service: UpdateProductService, **kwargs):
        super().__init__(**kwargs)
        self._update_product_service = update_product_service

    @property
    def update_product_service(self):
        return self._update_product_service

    def put(self, request: Request, product_id: int) -> Response:
        serializer = CheckIdSerializer(id=product_id, name="Product")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.update_product_service.update(token, request.user, product_id)
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


class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_product_service: DeleteProductService, **kwargs):
        super().__init__(**kwargs)
        self._delete_product_service = delete_product_service

    @property
    def delete_product_service(self):
        return self._delete_product_service

    def delete(self, request: Request, product_id: int) -> Response:
        serializer = CheckIdSerializer(id=product_id, name="Product")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.delete_product_service.delete(token, request.user, product_id)
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
