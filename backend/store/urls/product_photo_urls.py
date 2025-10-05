from django.urls import path

from store.service.product_photo_service import FindByIdProductPhotoService, FindAllForProductService, \
    CreateProductPhotoService, DeleteProductPhotoService
from store.views.product_photo_view import FindByIdProductPhotoView, FindAllForProductView, CreateProductPhotoView, \
    DeleteProductPhotoView

find_by_id_product_photo_service = FindByIdProductPhotoService()
find_all_for_product_service = FindAllForProductService()
create_service = CreateProductPhotoService()
delete_service = DeleteProductPhotoService()

urlpatterns = [
    path("find_by_id/<int:product_photo_id>/", FindByIdProductPhotoView.as_view(find_by_id_product_photo_service=find_by_id_product_photo_service),
         name="find_by_id_product_photo/<int:product_photo_id>"),
    path("find_all_for_product/<int:product_id>/", FindAllForProductView.as_view(find_all_for_product_service=find_all_for_product_service),
         name="find_all_for_product/<int:product_id>"),
    path("create/", CreateProductPhotoView.as_view(create_product_photo_service=create_service), name="create_product_photo"),
    path("delete/<int:product_photo_id>/", DeleteProductPhotoView.as_view(delete_product_photo_service=delete_service),
         name="delete_product_photo/<int:product_photo_id>"),
]