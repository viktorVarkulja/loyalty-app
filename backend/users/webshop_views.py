"""
Webshop API endpoints for external integration.
These are mock endpoints as specified in requirements.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import serializers

from users.models import User


class PointsBalanceSerializer(serializers.Serializer):
    """Serializer for points balance response."""
    user_id = serializers.CharField()
    email = serializers.CharField()
    points = serializers.IntegerField()


class UsePointsSerializer(serializers.Serializer):
    """Serializer for using points request."""
    points = serializers.IntegerField(required=True, min_value=1)
    reason = serializers.CharField(required=False, allow_blank=True)


class AddPointsSerializer(serializers.Serializer):
    """Serializer for adding points request."""
    points = serializers.IntegerField(required=True, min_value=1)
    reason = serializers.CharField(required=False, allow_blank=True)


class ApiResponseSerializer(serializers.Serializer):
    """Generic API response serializer."""
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = serializers.DictField(required=False)


@extend_schema(
    summary="Get user points balance (Webshop API)",
    description="Get the current points balance for the authenticated user.",
    responses={
        200: PointsBalanceSerializer,
        401: OpenApiResponse(description="Unauthorized")
    },
    tags=['Webshop API']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def webshop_get_points(request):
    """Get user's points balance (for webshop integration)."""
    user = request.user
    return Response({
        "success": True,
        "message": "Points retrieved successfully",
        "data": {
            "user_id": user.id,
            "email": user.email,
            "points": user.points
        }
    })


@extend_schema(
    summary="Use/deduct points (Webshop API)",
    description="Deduct points from the authenticated user's balance (e.g., during checkout).",
    request=UsePointsSerializer,
    responses={
        200: ApiResponseSerializer,
        400: OpenApiResponse(description="Validation error or insufficient points"),
        401: OpenApiResponse(description="Unauthorized")
    },
    tags=['Webshop API']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def webshop_use_points(request):
    """Deduct points from user's balance (for webshop integration)."""
    serializer = UsePointsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "message": "Validation error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user
    points_to_use = serializer.validated_data['points']
    reason = serializer.validated_data.get('reason', 'Webshop purchase')

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
            "reason": reason
        }
    })


@extend_schema(
    summary="Add points to user (Webshop API)",
    description="Add points to the authenticated user's balance (e.g., after purchase or promotion).",
    request=AddPointsSerializer,
    responses={
        200: ApiResponseSerializer,
        400: OpenApiResponse(description="Validation error"),
        401: OpenApiResponse(description="Unauthorized")
    },
    tags=['Webshop API']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def webshop_add_points(request):
    """Add points to user's balance (for webshop integration)."""
    serializer = AddPointsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "message": "Validation error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user
    points_to_add = serializer.validated_data['points']
    reason = serializer.validated_data.get('reason', 'Webshop promotion')

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
