from django.urls import path

from store.service.order_product_service import FindByIdOrderProductService, CreateOrderProductService, DeleteOrderProductService
from store.views.order_product_view import FindByIdOrderProductView, CreateOrderProductView, DeleteOrderProductView

find_by_id_order_product_service = FindByIdOrderProductService()
create_service = CreateOrderProductService()
delete_service = DeleteOrderProductService()


urlpatterns = [
    path("find_by_id/<int:order_product_id>/", FindByIdOrderProductView.as_view(
        find_by_id_order_product_service=find_by_id_order_product_service), name="find_by_id_order_product/<int:order_product_id>"),
    path("create/", CreateOrderProductView.as_view(create_order_product_service=create_service),
         name="create_order_product"),
    path("delete/<int:order_product_id>/", DeleteOrderProductView.as_view(delete_order_product_service=delete_service),
         name="delete_order_product/<int:order_product_id>"),
]
