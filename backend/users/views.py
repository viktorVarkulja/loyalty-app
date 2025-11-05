from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account with email, name, and password.",
        responses={
            201: OpenApiResponse(
                response=UserSerializer,
                description="User created successfully"
            ),
            400: OpenApiResponse(description="Bad request - validation error")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login endpoint with user data."""

    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="Login user",
        description="Authenticate user with email and password, returns JWT tokens and user data.",
        responses={
            200: OpenApiResponse(description="Login successful"),
            401: OpenApiResponse(description="Invalid credentials")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    summary="Get current user profile",
    description="Retrieve the authenticated user's profile information.",
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description="Not authenticated")
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    summary="Update user profile",
    description="Update the authenticated user's profile (name only).",
    request=UserSerializer,
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description="Not authenticated"),
        400: OpenApiResponse(description="Validation error")
    }
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """Update current user profile."""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
