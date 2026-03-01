from django.urls import path

from store.service.product_service import FindByIdProductService, FindAllProductsService, CreateProductService, \
    UpdateProductService, DeleteProductService
from store.views.product_view import FindByIdProductView, FindAllProductsView, CreateProductView, UpdateProductView, \
    DeleteProductView

find_by_id_product_service = FindByIdProductService()
find_all_products_service = FindAllProductsService()
create_service = CreateProductService()
update_service = UpdateProductService()
delete_service = DeleteProductService()

urlpatterns = [
    path("find_by_id/<int:product_id>/", FindByIdProductView.as_view(find_by_id_product_service=find_by_id_product_service),
         name="find_by_id_product"),
    path("find_all/", FindAllProductsView.as_view(find_all_products_service=find_all_products_service),
         name="find_all_products"),
    path("create/", CreateProductView.as_view(create_product_service=create_service), name="create_product"),
    path("update/<int:product_id>/", UpdateProductView.as_view(update_product_service=update_service),
         name="update_product"),
    path("delete/<int:product_id>/", DeleteProductView.as_view(delete_product_service=delete_service),
         name="delete_product"),
]
