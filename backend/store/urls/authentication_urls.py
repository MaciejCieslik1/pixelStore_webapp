from django.urls import path
from ..views.authentication_view import *

register_service = RegisterService()
login_service = LoginService()
logout_service = LogoutService()
verify_account_service = VerifyAccountService()
verify_token_service = VerifyTokenService()
refresh_token_service = RefreshTokenService()

urlpatterns = [
    path("register/", RegisterView.as_view(register_service=register_service), name="register"),
    path("login/", LoginView.as_view(login_service=login_service), name="login"),
    path('logout/', LogoutView.as_view(logout_service=logout_service), name='logout'),
    path("verify_account/", VerifyAccountView.as_view(verify_account_service=verify_account_service),
         name="verify_account"),
    path("verify_token/", VerifyTokenView.as_view(verify_token_service=verify_token_service),
         name="verify_token"),
    path("refresh_token/", RefreshTokenView.as_view(refresh_token_service=refresh_token_service),
         name="refresh_token"),
]
