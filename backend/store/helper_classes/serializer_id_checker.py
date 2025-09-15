class SerializerHelper:
    @staticmethod
    def return_id_error(id: int, error_messages: dict) -> str:
        if id is None:
            return error_messages["empty"]
        if not isinstance(id, int) or id < 1:
            return error_messages["not_positive_int"]
        return None

    @staticmethod
    def return_price_error(price: int | float) -> str:
        if price is None:
            return  "Shopping price cannot be empty."
        if (not isinstance(price, int) and not isinstance(price, float)) or price < 0.01 :
            return "Shopping price must be positive integer or decimal."
        if (isinstance(price, int) and price > 999999) or (isinstance(price, float) and price > 999999.99):
            return "Shopping price must be less than 1000000.00."
        return None
