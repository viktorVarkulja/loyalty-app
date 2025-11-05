"""
Webshop API endpoints for external integration.
These are mock endpoints as specified in requirements.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import serializers

from users.models import User
from products.models import ApiKey
from django.utils import timezone


class PointsBalanceSerializer(serializers.Serializer):
    """Serializer for points balance response."""
    user_id = serializers.CharField()
    email = serializers.CharField()
    points = serializers.IntegerField()


class UsePointsSerializer(serializers.Serializer):
    """Serializer for using points request."""
    user_id = serializers.CharField(required=True)
    points = serializers.IntegerField(required=True, min_value=1)
    order_id = serializers.CharField(required=False, allow_blank=True)


class AddPointsSerializer(serializers.Serializer):
    """Serializer for adding points request."""
    user_id = serializers.CharField(required=True)
    points = serializers.IntegerField(required=True, min_value=1)
    reason = serializers.CharField(required=False, allow_blank=True)


class ApiResponseSerializer(serializers.Serializer):
    """Generic API response serializer."""
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = serializers.DictField(required=False)


def validate_api_key(request):
    """
    Validate API key from Authorization header.
    Returns (is_valid, user, error_response)
    """
    auth_header = request.headers.get('Authorization', '')

    if not auth_header.startswith('Bearer '):
        return False, None, Response(
            {"success": False, "message": "Invalid Authorization header format. Use 'Bearer <api_key>'"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    api_key = auth_header.replace('Bearer ', '').strip()

    try:
        api_key_obj = ApiKey.objects.get(key=api_key, active=True)
        api_key_obj.last_used = timezone.now()
        api_key_obj.save()
        return True, api_key_obj.user, None
    except ApiKey.DoesNotExist:
        return False, None, Response(
            {"success": False, "message": "Invalid or inactive API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )


@extend_schema(
    summary="Get user points balance (Webshop API)",
    description="""
    Get the current points balance for a specific user.

    **Authentication**: Requires valid API key in Authorization header.

    **Header**: `Authorization: Bearer <your_api_key>`
    """,
    parameters=[
        OpenApiParameter(
            name='user_id',
            description='User ID to check points for',
            required=True,
            type=str,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='Authorization',
            description='API Key (Bearer token)',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ],
    responses={
        200: PointsBalanceSerializer,
        400: OpenApiResponse(description="Missing user_id parameter"),
        401: OpenApiResponse(description="Invalid API key"),
        404: OpenApiResponse(description="User not found")
    },
    tags=['Webshop API']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def webshop_get_points(request):
    """Get user's points balance (for webshop integration)."""
    # Validate API key
    is_valid, api_user, error_response = validate_api_key(request)
    if not is_valid:
        return error_response

    user_id = request.query_params.get('user_id')

    if not user_id:
        return Response(
            {"success": False, "message": "user_id parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id)
        return Response({
            "success": True,
            "message": "Points retrieved successfully",
            "data": {
                "user_id": user.id,
                "email": user.email,
                "points": user.points
            }
        })
    except User.DoesNotExist:
        return Response(
            {"success": False, "message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(
    summary="Use/deduct points (Webshop API)",
    description="""
    Deduct points from a user's balance (e.g., during checkout).

    **Authentication**: Requires valid API key in Authorization header.

    **Header**: `Authorization: Bearer <your_api_key>`
    """,
    request=UsePointsSerializer,
    parameters=[
        OpenApiParameter(
            name='Authorization',
            description='API Key (Bearer token)',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ],
    responses={
        200: ApiResponseSerializer,
        400: OpenApiResponse(description="Validation error or insufficient points"),
        401: OpenApiResponse(description="Invalid API key"),
        404: OpenApiResponse(description="User not found")
    },
    tags=['Webshop API']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def webshop_use_points(request):
    """Deduct points from user's balance (for webshop integration)."""
    # Validate API key
    is_valid, api_user, error_response = validate_api_key(request)
    if not is_valid:
        return error_response

    serializer = UsePointsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "message": "Validation error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_id = serializer.validated_data['user_id']
    points_to_use = serializer.validated_data['points']
    order_id = serializer.validated_data.get('order_id', '')

    try:
        user = User.objects.get(id=user_id)

        if user.points < points_to_use:
            return Response(
                {
                    "success": False,
                    "message": f"Insufficient points. User has {user.points} points, but {points_to_use} requested"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deduct points
        user.points -= points_to_use
        user.save()

        return Response({
            "success": True,
            "message": f"Successfully deducted {points_to_use} points",
            "data": {
                "user_id": user.id,
                "points_used": points_to_use,
                "remaining_points": user.points,
                "order_id": order_id
            }
        })

    except User.DoesNotExist:
        return Response(
            {"success": False, "message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(
    summary="Add points to user (Webshop API)",
    description="""
    Add points to a user's balance (e.g., after purchase or promotion).

    **Authentication**: Requires valid API key in Authorization header.

    **Header**: `Authorization: Bearer <your_api_key>`
    """,
    request=AddPointsSerializer,
    parameters=[
        OpenApiParameter(
            name='Authorization',
            description='API Key (Bearer token)',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ],
    responses={
        200: ApiResponseSerializer,
        400: OpenApiResponse(description="Validation error"),
        401: OpenApiResponse(description="Invalid API key"),
        404: OpenApiResponse(description="User not found")
    },
    tags=['Webshop API']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def webshop_add_points(request):
    """Add points to user's balance (for webshop integration)."""
    # Validate API key
    is_valid, api_user, error_response = validate_api_key(request)
    if not is_valid:
        return error_response

    serializer = AddPointsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "message": "Validation error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_id = serializer.validated_data['user_id']
    points_to_add = serializer.validated_data['points']
    reason = serializer.validated_data.get('reason', 'Webshop promotion')

    try:
        user = User.objects.get(id=user_id)

        # Add points
        user.points += points_to_add
        user.save()

        return Response({
            "success": True,
            "message": f"Successfully added {points_to_add} points",
            "data": {
                "user_id": user.id,
                "points_added": points_to_add,
                "total_points": user.points,
                "reason": reason
            }
        })

    except User.DoesNotExist:
        return Response(
            {"success": False, "message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
