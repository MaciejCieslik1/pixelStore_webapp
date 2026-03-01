from django.urls import path

from store.service.order_return_service import FindByIdOrderReturnService, CreateOrderReturnService, \
    UpdateOrderReturnService
from store.views.order_return_view import FindByIdOrderReturnView, CreateOrderReturnView, UpdateOrderReturnView

find_by_id_order_return_service = FindByIdOrderReturnService()
create_service = CreateOrderReturnService()
update_service = UpdateOrderReturnService()

urlpatterns = [
    path("find_by_id/<int:order_return_id>/", FindByIdOrderReturnView.as_view(
        find_by_id_order_return_service=find_by_id_order_return_service), name="find_by_id_order_return"),
    path("create/", CreateOrderReturnView.as_view(create_order_return_service=create_service),
         name="create_order_return"),
    path("update/<int:order_return_id>/", UpdateOrderReturnView.as_view(update_order_return_service=update_service),
         name="update_order_return"),
]