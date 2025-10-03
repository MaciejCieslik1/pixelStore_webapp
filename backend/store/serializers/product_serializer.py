from store.serializers.check_username_serializer import CheckUsernameSerializer


class FindAllProductsSerializer:
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
        return (self._validate_owner_username() and self._validate_name() and
            self._validate_price(self.data.get("min_price"), "min_price") and
            self._validate_price(self.data.get("max_price"), "max_price") and self._validate_status() and
            self._validate_ordering_field() and self._validate_order() and self._validate_page() and self._validate_page_size())

    def _validate_owner_username(self) -> bool:
        username = self.data.get("owner_username")
        if username is None:
            self.validated_data["owner_username"] = None
            return True
        username_serializer = CheckUsernameSerializer(username)
        result = username_serializer.is_valid()
        self.validated_data["owner_username"] = username_serializer.validated_username
        if username_serializer.error:
            self.errors["owner_username"] = username_serializer.error
        return result

    def _validate_name(self) -> bool:
        name = self.data.get("name")
        if name is None:
            self.validated_data["name"] = None
            return True
        if not name:
            self.errors["name"] = "Name cannot be empty."
        elif not isinstance(name, str):
            self.errors["name"] = "Name must be a string."
        elif len(name.strip()) > 32:
            self.errors["name"] = "Name cannot be longer than 32 characters."
        else:
            self.validated_data["name"] = name.strip()
            return True
        return False

    def _validate_price(self, price: int | float, label: str) -> bool:
        if price is None:
            self.validated_data["price"] = None
            return True
        elif (not isinstance(price, int) and not isinstance(price, float)) or price < 0.01:
            self.errors[label] = f"{label.capitalize()} price must be positive integer or decimal."
        elif (isinstance(price, int) and price > 999999) or (isinstance(price, float) and price > 999999.99):
            self.errors[label] = f"{label.capitalize()} price must be less than 1000000.00."
        else:
            self.validated_data[label] = price
            return True
        return False

    def _validate_status(self):
        status = self.data.get("status")
        if status is None:
            self.validated_data["status"] = None
            return True
        if status.strip().lower() not in ("available", "unavailable", "archived"):
            self.errors["status"] = "Status must be one of following: 'available', 'unavailable', 'archived'."
            return False
        self.validated_data["status"] = status.strip().lower()
        return True

    def _validate_ordering_field(self):
        ordering_field = self.data.get("ordering_field")
        if ordering_field is None:
            self.validated_data["ordering_field"] = None
            return True
        if ordering_field.strip().lower() not in ("name", "price", "status"):
            self.errors["ordering_field"] = "Ordering field must be one of following: 'name', 'price', 'status'."
            return False
        self.validated_data["ordering_field"] = ordering_field.strip().lower()
        return True

    def _validate_order(self):
        order = self.data.get("order", "desc")
        if order:
            if isinstance(order, str):
                order = order.strip().lower()
            if order not in ["asc", "desc"]:
                self.errors["order"] = "Order must be: 'asc' or 'desc'."
                return False
            self.validated_data["order"] = order
            return True
        self.validated_data["order"] = "desc"
        return True

    def _validate_page(self):
        page = self.data.get("page", 1)
        if page or page == 0:
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


class CreateProductSerializer:
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
        return (self._validate_owner_username() and self._validate_name() and self._validate_description() and
                self._validate_price() and self._validate_amount() and self._validate_color() and self._validate_weight() and
                self._validate_length() and self._validate_width() and self._validate_height() and
                self._validate_guarantee_period() and self._validate_status())

    def _validate_owner_username(self) -> bool:
        username_serializer = CheckUsernameSerializer(self.data.get("owner_username"))
        result = username_serializer.is_valid()
        self.validated_data["owner_username"] = username_serializer.validated_username
        if username_serializer.error:
            self.errors["owner_username"] = username_serializer.error
        return result

    def _validate_name(self) -> bool:
        name = self.data.get("name")
        if not name:
            self.errors["name"] = "Product name cannot be empty."
        elif not isinstance(name, str):
            self.errors["name"] = "Product name must be a string."
        elif len(name.strip()) > 32:
            self.errors["name"] = "Product name cannot be longer than 32 characters."
        else:
            self.validated_data["name"] = name.strip()
            return True
        return False

    def _validate_description(self) -> bool:
        description = self.data.get("description")
        if not description:
            self.errors["description"] = "Description cannot be empty."
        elif not isinstance(description, str):
            self.errors["description"] = "Description must be string."
        elif len(description) > 1024:
            self.errors["description"] = "Description must be less than 1025 characters."
        else:
            self.validated_data["description"] = description.strip()
            return True
        return False

    def _validate_price(self) -> bool:
        price = self.data.get("price")
        if price is None:
            self.errors["price"] = "Price cannot be empty."
        elif (not isinstance(price, int) and not isinstance(price, float)) or price < 0.01:
            self.errors["price"] = "Price must be positive integer or decimal."
        elif (isinstance(price, int) and price > 999999) or (isinstance(price, float) and price > 999999.99):
            self.errors["price"] = "Price must be less than 1000000.00."
        else:
            self.validated_data["price"] = price
            return True
        return False

    def _validate_status(self):
        status = self.data.get("status")
        if not status or status.strip().lower() not in ("available", "unavailable", "archived"):
            self.errors["status"] = "Status must be one of following: 'available', 'unavailable', 'archived'."
            return False
        self.validated_data["status"] = status.strip().lower()
        return True

    def _validate_amount(self) -> bool:
        amount = self.data.get("amount")
        if amount is None:
            self.errors["amount"] = "Amount cannot be empty."
        elif not isinstance(amount, int) or amount < 0:
            self.errors["amount"] = "Amount must be positive integer."
        elif amount > 999:
            self.errors["amount"] = "Amount must be less than 1000000.00."
        else:
            self.validated_data["amount"] = amount
            return True
        return False

    def _validate_color(self) -> bool:
        color = self.data.get("color")
        if not color:
            self.errors["color"] = "Color cannot be empty."
        elif not isinstance(color, str):
            self.errors["color"] = "Color must be string."
        elif len(color) > 32:
            self.errors["color"] = "Color length must be less than 33 characters."
        else:
            self.validated_data["color"] = color.strip()
            return True
        return False

    def _validate_weight(self) -> bool:
        weight = self.data.get("weight")
        if weight is None:
            self.errors["weight"] = "Weight cannot be empty."
        elif (not isinstance(weight, int) and not isinstance(weight, float)) or weight < 0.01:
            self.errors["weight"] = "Weight must be positive integer or decimal."
        elif (isinstance(weight, int) and weight > 99) or (isinstance(weight, float) and weight > 99.99):
            self.errors["weight"] = "Weight must be less than 100.00."
        else:
            self.validated_data["weight"] = weight
            return True
        return False

    def _validate_length(self) -> bool:
        length = self.data.get("length")
        if length is None:
            self.errors["length"] = "Length cannot be empty."
        elif (not isinstance(length, int) and not isinstance(length, float)) or length < 0.01:
            self.errors["length"] = "Length must be positive integer or decimal."
        elif (isinstance(length, int) and length > 999) or (isinstance(length, float) and length > 999.99):
            self.errors["length"] = "Length must be less than 1000.00."
        else:
            self.validated_data["length"] = length
            return True
        return False

    def _validate_width(self) -> bool:
        width = self.data.get("width")
        if width is None:
            self.errors["width"] = "Width cannot be empty."
        elif (not isinstance(width, int) and not isinstance(width, float)) or width < 0.01:
            self.errors["width"] = "Width must be positive integer or decimal."
        elif (isinstance(width, int) and width > 999) or (isinstance(width, float) and width > 999.99):
            self.errors["width"] = "Width must be less than 1000.00."
        else:
            self.validated_data["width"] = width
            return True
        return False

    def _validate_height(self) -> bool:
        height = self.data.get("height")
        if height is None:
            self.errors["height"] = "Height cannot be empty."
        elif (not isinstance(height, int) and not isinstance(height, float)) or height < 0.01:
            self.errors["height"] = "Height must be positive integer or decimal."
        elif (isinstance(height, int) and height > 999) or (isinstance(height, float) and height > 999.99):
            self.errors["height"] = "Height must be less than 1000.00."
        else:
            self.validated_data["height"] = height
            return True
        return False

    def _validate_guarantee_period(self) -> bool:
        guarantee_period = self.data.get("guarantee_period")
        if guarantee_period is None:
            self.errors["guarantee_period"] = "Guarantee period cannot be empty."
        elif not isinstance(guarantee_period, int) or guarantee_period < 0:
            self.errors["guarantee_period"] = "Guarantee period must be positive integer."
        elif guarantee_period > 100:
            self.errors["guarantee_period"] = "Guarantee period must be less than 10."
        else:
            self.validated_data["guarantee_period"] = guarantee_period
            return True
        return False
