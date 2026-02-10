from django.urls import path

from store.service.product_review_service import FindByIdProductReviewService, FindAllProductReviewsService, \
    FindAllFromUserProductReviewsService, CreateProductReviewService, DeleteProductReviewService
from store.views.product_review_view import FindAllProductReviewsView, FindAllFromUserProductReviewsView, \
    CreateProductReviewView, DeleteProductReviewView, FindByIdProductReviewView

find_by_id_product_review_service = FindByIdProductReviewService()
find_all_product_reviews_service = FindAllProductReviewsService()
find_all_from_user_product_reviews_service = FindAllFromUserProductReviewsService()
create_service = CreateProductReviewService()
delete_service = DeleteProductReviewService()

urlpatterns = [
    path("find_by_id/<int:product_review_id>/", FindByIdProductReviewView.as_view(
        find_by_id_product_review_service=find_by_id_product_review_service),
        name="find_by_id_product_review/<int:product_review_id>"),
    path("find_all_for_product/<int:product_id>/", FindAllProductReviewsView.as_view(
        find_all_product_reviews_service=find_all_product_reviews_service),
         name="find_all_product_reviews/<int:product_id>"),
    path("find_all_from_user/<str:reviewer_username>/", FindAllFromUserProductReviewsView.as_view(
        find_all_from_user_product_reviews_service=find_all_from_user_product_reviews_service),
         name="find_all_from_user_product_reviews/<str:reviewer_username>"),
    path("create/", CreateProductReviewView.as_view(create_product_review_service=create_service),
         name="create_review_product"),
    path("delete/<int:product_review_id>/", DeleteProductReviewView.as_view(delete_product_review_service=delete_service),
         name="delete_product/<int:product_review_id>"),
]
