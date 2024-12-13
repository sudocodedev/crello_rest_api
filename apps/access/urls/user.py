from apps.access.views import (
    LoginAPIView, SignUpAPIView, LogoutAPIView, RefreshTokenAPIView,
    UserViewset, MEAPIView)
from apps.common.router import router
from django.urls import path

app_name = "access"

API_URL_PREFIX = "api/access/"
USER_URL_PREFIX = "api/users/"
ME_URL_PREFIX = "api/me/"


# USERS
router.register(f"{USER_URL_PREFIX}read", UserViewset)

urlpatterns = [
    # Authentication
    path(f'{API_URL_PREFIX}signup/', SignUpAPIView.as_view(), name="sign-up"),
    path(f'{API_URL_PREFIX}login/', LoginAPIView.as_view(), name="login"),
    path(f'{API_URL_PREFIX}logout/', LogoutAPIView.as_view(), name="logout"),
    path(f'{API_URL_PREFIX}refresh-token/', RefreshTokenAPIView.as_view(), name="refresh-token"),

    # Me
    path('api/me/', MEAPIView.as_view(), name="me")
] 
urlpatterns += router.urls