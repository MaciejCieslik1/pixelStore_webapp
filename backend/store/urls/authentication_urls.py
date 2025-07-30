from django.urls import path
from backend.store.views.authentication_view import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify/", VerifyTokenView.as_view(), name="verify"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh")
]
