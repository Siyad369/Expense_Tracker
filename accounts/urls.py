from django.urls import path

from .views import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # REGISTER
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    # LOGIN
    path(
        'login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    # REFRESH TOKEN
    path(
        'refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]