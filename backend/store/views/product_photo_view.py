from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_id_serializer import CheckIdSerializer
from store.serializers.product_photo_serializer import FindAllProductPhotosSerializer, CreateProductPhotoSerializer
from store.service.product_photo_service import FindByIdProductPhotoService, FindAllForProductService, \
    CreateProductPhotoService, DeleteProductPhotoService


class FindByIdProductPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_product_photo_service: FindByIdProductPhotoService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_product_photo_service = find_by_id_product_photo_service

    @property
    def find_by_id_product_photo_service(self):
        return self._find_by_id_product_photo_service

    def get(self, request: Request, product_photo_id: int) -> Response:
        serializer = CheckIdSerializer(id=product_photo_id, name="Product photo")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                product_found = self.find_by_id_product_photo_service.find_by_id(token, request.user, product_photo_id)
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


class FindAllForProductView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_for_product_service: FindAllForProductService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_for_product_service = find_all_for_product_service

    @property
    def find_all_for_product_service(self):
        return self._find_all_for_product_service

    def get(self, request: Request) -> Response:
        serializer = FindAllProductPhotosSerializer(data=request.query_params)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                products_found = self.find_all_for_product_service.find_all_for_product(token, request.user, serializer.validated_data)
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


class CreateProductPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_product_photo_service: CreateProductPhotoService, **kwargs):
        super().__init__(**kwargs)
        self._create_product_photo_service = create_product_photo_service

    @property
    def create_product_photo_service(self):
        return self._create_product_photo_service

    def post(self, request: Request) -> Response:
        serializer = CreateProductPhotoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.create_product_photo_service.create(token, request.user, serializer.validated_data)
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


class DeleteProductPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_product_photo_service: DeleteProductPhotoService, **kwargs):
        super().__init__(**kwargs)
        self._delete_product_photo_service = delete_product_photo_service

    @property
    def delete_product_photo_service(self):
        return self._delete_product_photo_service

    def delete(self, request: Request, product_photo_id: int) -> Response:
        serializer = CheckIdSerializer(id=product_photo_id, name="Product")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.delete_product_photo_service.delete(token, request.user, product_photo_id)
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
