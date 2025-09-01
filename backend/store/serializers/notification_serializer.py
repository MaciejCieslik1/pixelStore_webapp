from datetime import datetime

class FindAllNotificationsSerializer:
    def __init__(self, data: dict):
        self._data = data
        self._validated_data = {}
        self._errors = {}

    @property
    def data(self):
        return self._data

    @property
    def validated_data(self):
        return self._validated_data

    @property
    def errors(self):
        return self._errors

    def is_valid(self) -> bool:
        return True

    # def is_valid(self) -> bool:
    #     return (self._validate_date_from() and self._validate_date_to() and self._validate_order() and self._validate_page()
    #         and self._validate_page_size())
    #
    # def _validate_date_from(self):
    #     date_from = self.data.get("date_from")
    #     if date_from:
    #         try:
    #             parsed = datetime.strptime(date_from, "%Y-%m-%d").date()
    #             self._validated_data["date_from"] = parsed
    #         except ValueError:
    #             self._errors["date_from"] = "Invalid date format. Use YYYY-MM-DD."
    #             return False
    #     else:
    #         self._validated_data["date_from"] = None
    #     return True
    #
    # def _validate_date_to(self):
    #     date_to = self.data.get("date_to")
    #     if date_to:
    #         try:
    #             parsed = datetime.strptime(date_to, "%Y-%m-%d").date()
    #             self._validated_data["date_to"] = parsed
    #         except ValueError:
    #             self._errors["date_to"] = "Invalid date format. Use YYYY-MM-DD."
    #             return False
    #     else:
    #         self._validated_data["date_to"] = None
    #     return True
    #
    # def _validate_order(self):
    #     order = self.data.get("order", "desc").lower()
    #     if order not in ["asc", "desc"]:
    #         self._errors["order"] = "Order must be 'asc' or 'desc'."
    #         return False
    #     self._validated_data["order"] = order
    #     return True
    #
    # def _validate_page(self):
    #     page = self.data.get("page", 1)
    #     try:
    #         page = int(page)
    #         if page < 1:
    #             raise ValueError
    #         self._validated_data["page"] = page
    #     except ValueError:
    #         self._errors["page"] = "Page must be a positive integer."
    #         return False
    #     return True
    #
    # def _validate_page_size(self):
    #     page_size = self.data.get("page_size", 10)
    #     try:
    #         page_size = int(page_size)
    #         if page_size < 1 or page_size > 100:
    #             raise ValueError
    #         self._validated_data["page_size"] = page_size
    #     except ValueError:
    #         self._errors["page_size"] = "Page size must be between 1 and 100."
    #         return False
    #     return True


class CreateNotificationSerializer:
    def __init__(self, data: dict):
        self._data = data
        self._validated_data = {}
        self._errors = {}

    @property
    def data(self):
        return self._data

    @property
    def validated_data(self):
        return self._validated_data

    @property
    def errors(self):
        return self._errors

    def is_valid(self) -> bool:
        return True


class DeleteNotificationSerializer:
    def __init__(self, data: dict):
        self._data = data
        self._validated_data = {}
        self._errors = {}

    @property
    def data(self):
        return self._data

    @property
    def validated_data(self):
        return self._validated_data

    @property
    def errors(self):
        return self._errors

    def is_valid(self) -> bool:
        return True
