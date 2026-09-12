from rest_framework import serializers
from main.models import User, ClientProfile


class ClientRegistrationSerializer(serializers.Serializer):
    """Validates registration input and creates a User + associated ClientProfile."""
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=User.Role.CLIENT,
        )
        return ClientProfile.objects.create(user=user, full_name=validated_data['name'])
