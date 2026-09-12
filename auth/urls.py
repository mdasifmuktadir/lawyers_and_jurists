from django.urls import path
from .views import RegisterClientView, LoginClientView, ClientCasesView, ChangePasswordView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterClientView.as_view(), name='register-client'),
    path('login/', LoginClientView.as_view(), name='login-client'),
    path('cases/', ClientCasesView.as_view(), name='client-cases'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
     path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
