from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, CategoryNotFoundError, CategoryNameAlreadyOccupiedError
from store.helper_classes.authentication_helper import TokenUtils
from store.serializers.category_serializer import FindCategoryByNameSerializer, CreateCategorySerializer
from store.service.category_service import FindCategoryByNameService, FindAllCategoriesService, CreateCategoryService


class FindCategoryByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_category_by_name_service: FindCategoryByNameService, **kwargs):
        super().__init__(**kwargs)
        self._find_category_by_name_service = find_category_by_name_service

    @property
    def find_category_by_name_service(self):
        return self._find_category_by_name_service

    def get(self, request: Request, name: str) -> Response:
        serializer = FindCategoryByNameSerializer(name=name)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                category_found = self.find_category_by_name_service.find_by_name(token, request.user, name)
                return Response(category_found, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except CategoryNotFoundError as e:
                return Response(
                    {"error": "Category name not found.", "details": str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class FindAllCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, find_all_categories_service: FindAllCategoriesService, **kwargs):
        super().__init__(**kwargs)
        self._find_all_categories_service = find_all_categories_service

    @property
    def find_all_categories_service(self):
        return self._find_all_categories_service

    def get(self, request: Request) -> Response:
        try:
            token = TokenUtils.get_jwt_token_from_request(request)
            category_found = self.find_all_categories_service.find_all(token, request.user)
            return Response(category_found, status=status.HTTP_200_OK)
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


class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, create_category_service: CreateCategoryService, **kwargs):
        super().__init__(**kwargs)
        self._create_category_service = create_category_service

    @property
    def create_category_service(self):
        return self._create_category_service

    def post(self, request: Request) -> Response:
        serializer = CreateCategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = TokenUtils.get_jwt_token_from_request(request)
                self.create_category_service.create(token, request.user, serializer.validated_data)
                return Response({"msg": "Category created successfully."}, status=status.HTTP_200_OK)
            except (IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError,
                    TokenExpiredByReplacementError) as e:
                return Response(
                    {"error": "Access token error.", "details": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except CategoryNameAlreadyOccupiedError as e:
                return Response(
                    {"error": "Category name is already occupied.", "details": str(e)},
                    status=status.HTTP_409_CONFLICT
                )
            except Exception as e:
                return Response(
                    {"error": "Unexpected error.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
