from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'points', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password_confirm']

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """Create a new user."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer that includes user data."""

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user data to response
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'name': self.user.name,
            'role': self.user.role,
            'points': self.user.points,
        }

        return data
