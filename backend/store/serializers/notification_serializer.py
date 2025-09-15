from datetime import datetime

from store.helper_classes.authentication_helper import DataValidator


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
        return (self._validate_date_from() and self._validate_date_to() and self._validate_order() and self._validate_page()
            and self._validate_page_size())

    def _validate_date_from(self):
        date_from = self.data.get("date_from")
        if isinstance(date_from, str):
            date_from = date_from.strip()
        if date_from:
            try:
                parsed = datetime.strptime(date_from, "%Y-%m-%d").date()
                self.validated_data["date_from"] = parsed
            except ValueError:
                self.errors["date_from"] = "Date must have YYYY-MM-DD format."
                return False
        else:
            self.validated_data["date_from"] = None
        return True

    def _validate_date_to(self):
        date_to = self.data.get("date_to")
        if isinstance(date_to, str):
            date_to = date_to.strip()
        if date_to:
            try:
                parsed = datetime.strptime(date_to, "%Y-%m-%d").date()
                self.validated_data["date_to"] = parsed
            except ValueError:
                self.errors["date_to"] = "Date must have YYYY-MM-DD format."
                return False
        else:
            self.validated_data["date_to"] = None
        return True

    def _validate_order(self):
        order = self.data.get("order", "desc")
        if order:
            if isinstance(order, str):
                order = order.strip().lower()
            if order not in ["asc", "desc"]:
                self.errors["order"] = "Order must be 'asc' or 'desc'."
                return False
            self.validated_data["order"] = order
            return True
        self.validated_data["order"] = "desc"
        return True

    def _validate_page(self):
        page = self.data.get("page", 1)
        if page or page == 0 :
            try:
                page = int(page)
                if page < 1:
                    raise ValueError
                self.validated_data["page"] = page
            except ValueError:
                self.errors["page"] = "Page number must be a positive integer."
                return False
            return True
        self.validated_data["page"] = 1
        return True

    def _validate_page_size(self):
        page_size = self.data.get("page_size", 10)
        if page_size or page_size == 0:
            try:
                page_size = int(page_size)
                if page_size < 1 or page_size > 100:
                    raise ValueError
                self.validated_data["page_size"] = page_size
            except ValueError:
                self.errors["page_size"] = "Page size must be between 1 and 100."
                return False
            return True
        self.validated_data["page_size"] = 10
        return True


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
        return self._validate_username() and self._validate_text()

    def _validate_username(self):
        username = self._data.get("username")
        if not isinstance(username, str):
            self.errors["username"] = "Username must be string."
            return False
        username = username.strip()
        if not username:
            self.errors["username"] = "Username is not provided."
            return False
        self.validated_data["username"] = username
        return True

    def _validate_text(self):
        text = self._data.get("text")
        if isinstance(text, str):
            text = text.strip()
        if not text:
            self.errors["text"] = "Text is not provided."
            return False
        if len(text) > 1024:
            self.errors["text"] = "Text cannot be longer than 1024 characters."
            return False
        self._validated_data["text"] = text
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
        notification_id = self.data.get("notification_id")
        try:
            notification_id = int(notification_id)
            if notification_id < 1:
                raise ValueError
            self.validated_data["notification_id"] = notification_id
            return True
        except (TypeError, ValueError):
            self.errors["notification_id"] = "Notification id must be a positive integer and exist."
            return False
