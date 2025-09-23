class PageSerializer:
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
        return self._validate_page() and self._validate_page_size()

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