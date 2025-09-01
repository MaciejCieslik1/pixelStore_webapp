from datetime import date
from typing import Optional

from store.models import User


class FindAllNotificationsService:
    def find_all(self, token: str, date_from: Optional[date] = None, date_to: Optional[date] = None, order: str = "desc",
                 page: int = 1, page_size: int = 10):
        pass


class CreateNotificationService:
    def create(self, token: str, user: User, data: dict):
        pass


class DeleteNotificationService:
    def delete(self, token: str, user: User, data: dict):
        pass
