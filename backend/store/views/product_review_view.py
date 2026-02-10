from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.check_id_serializer import CheckIdSerializer
from store.serializers.check_username_serializer import CheckUsernameSerializer
from store.serializers.product_review_serializer import FindAllProductReviewsSerializer, \
    FindAllFromUserProductReviewsSerializer, CreateProductReviewSerializer
from store.service.product_review_service import FindByIdProductReviewService, FindAllProductReviewsService, \
    FindAllFromUserProductReviewsService, CreateProductReviewService, DeleteProductReviewService


class FindByIdProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_by_id_product_review_service: FindByIdProductReviewService, **kwargs):
        super().__init__(**kwargs)
        self._find_by_id_product_review_service = find_by_id_product_review_service

    @property
    def find_by_id_product_review_service(self):
        return self._find_by_id_product_review_service

    def get(self, request: Request, product_review_id: int) -> Response:
        serializer = CheckIdSerializer(id=product_review_id, name="Product review")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                product_review_found = self.find_by_id_product_review_service.find_by_id(token, request.user,
                                                                                       product_review_id)
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


class FindAllProductReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_product_reviews_service: FindAllProductReviewsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_product_reviews_service = find_all_product_reviews_service

    @property
    def find_all_product_reviews_service(self):
        return self._find_all_product_reviews_service

    def get(self, request: Request, product_id: int) -> Response:
        id_serializer = CheckIdSerializer(id=product_id, name="Product")
        serializer = FindAllProductReviewsSerializer(data=request.query_params)
        if serializer.is_valid() and id_serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                validated_data = serializer.validated_data
                validated_data["product_id"] = product_id
                product_reviews_found = self.find_all_product_reviews_service.find_all(token, request.user, validated_data)
                return Response(product_reviews_found, status=status.HTTP_200_OK)
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


class FindAllFromUserProductReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_from_user_product_reviews_service: FindAllFromUserProductReviewsService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_from_user_product_reviews_service = find_all_from_user_product_reviews_service

    @property
    def find_all_from_user_product_reviews_service(self):
        return self._find_all_from_user_product_reviews_service

    def get(self, request: Request, reviewer_username: str) -> Response:
        username_serializer = CheckUsernameSerializer(username=reviewer_username)
        serializer = FindAllFromUserProductReviewsSerializer(data=request.query_params)
        if serializer.is_valid() and username_serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                validated_data = serializer.validated_data
                validated_data["reviewer_username"] = reviewer_username
                product_reviews_found = self.find_all_from_user_product_reviews_service.find_all(token, request.user,
                                                                                                 validated_data)
                return Response(product_reviews_found, status=status.HTTP_200_OK)
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


class CreateProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_product_review_service: CreateProductReviewService, **kwargs):
        super().__init__(**kwargs)
        self._create_product_review_service = create_product_review_service

    @property
    def create_product_review_service(self):
        return self._create_product_review_service

    def post(self, request: Request) -> Response:
        serializer = CreateProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.create_product_review_service.create(token, request.user, serializer.validated_data)
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


class DeleteProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, delete_product_review_service: DeleteProductReviewService, **kwargs):
        super().__init__(**kwargs)
        self._delete_product_review_service = delete_product_review_service

    @property
    def delete_product_review_service(self):
        return self._delete_product_review_service

    def delete(self, request: Request, product_review_id: int) -> Response:
        serializer = CheckIdSerializer(id=product_review_id, name="Product")
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                communicate = self.delete_product_review_service.delete(token, request.user, product_review_id)
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
