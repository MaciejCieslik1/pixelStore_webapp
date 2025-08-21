from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from store.service.address_service import FindAddressService, UpdateAddressService


class FindAddressView(APIView):
    def __init__(self, find_address_service: FindAddressService, **kwargs):
        super().__init__(**kwargs)
        self._find_address_service = find_address_service

    @property
    def find_address_service(self):
        return self._find_address_service

    def get(self, request: Request) -> Response:
        pass


class UpdateAddressView(APIView):
    def __init__(self, update_address_service: UpdateAddressService, **kwargs):
        super().__init__(**kwargs)
        self._update_address_service = update_address_service

    @property
    def update_address_service(self):
        return self._update_address_service

    def put(self, request: Request) -> Response:
        pass