from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from main.serializers import CaseSerializer, ClientProfileSerializer
from .serializers import ClientRegistrationSerializer


class RegisterClientView(APIView):
    """Creates a User and an associated ClientProfile from name, email and password."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ClientRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_profile = serializer.save()
        return Response(
            ClientProfileSerializer(client_profile).data,
            status=status.HTTP_201_CREATED,
        )


class LoginClientView(APIView):
    """Authenticates a client and returns JWT access and refresh tokens."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password) or authenticate(
            request, email=email, password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not hasattr(user, "client_profile"):
            return Response(
                {"error": "This account does not have a client profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "client": ClientProfileSerializer(user.client_profile).data,
            },
            status=status.HTTP_200_OK,
        )


class ClientCasesView(APIView):
    """Returns the cases associated with the authenticated client."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cases = request.user.client_profile.cases.all()
        return Response(CaseSerializer(cases, many=True).data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """Updates the password of the authenticated user given new_password and confirm_password."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response(
                {"error": "new_password and confirm_password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != confirm_password:
            return Response(
                {"error": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(new_password, user=request.user)
        except ValidationError as exc:
            return Response({"error": exc.messages}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()

        return Response(
            {"message": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """Logs out the authenticated user by blacklisting their refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
