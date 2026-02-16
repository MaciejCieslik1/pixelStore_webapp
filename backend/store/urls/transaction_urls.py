from django.urls import path

from store.service.transaction_service import FindByIdTransactionService, FindAllMineTransactionsService, \
    CreateTransactionService, UpdateTransactionService
from store.views.transaction_view import FindByIdTransactionView, FindAllMineTransactionsView, UpdateTransactionView, \
    CreateTransactionView

find_by_id_transaction_service = FindByIdTransactionService()
find_all_mine_transactions_service = FindAllMineTransactionsService()
create_service = CreateTransactionService()
update_service = UpdateTransactionService()

urlpatterns = [
    path("find_by_id/<int:transaction_id>/", FindByIdTransactionView.as_view(
        find_by_id_transaction_service=find_by_id_transaction_service), name="find_by_id/<int:transaction_id>"),
    path("find_all_mine/", FindAllMineTransactionsView.as_view(
        find_all_mine_transactions_service=find_all_mine_transactions_service), name="find_all_mine_transactions"),
    path("create/", CreateTransactionView.as_view(create_transaction_service=create_service), name="create_transaction"),
    path("update/<int:transaction_id>/", UpdateTransactionView.as_view(update_transaction_service=update_service),
         name="update_transaction/<int:transaction_id>")
]
