from rest_framework import serializers
from django.utils import timezone
from .models import ReviewRequest
from users.serializers import UserSerializer


class ReviewRequestSerializer(serializers.ModelSerializer):
    """Serializer for ReviewRequest model."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = ReviewRequest
        fields = [
            'id', 'user', 'product_name', 'receipt_data',
            'status', 'admin_comment', 'points_awarded',
            'created_at', 'updated_at', 'reviewed_at'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'admin_comment',
            'points_awarded', 'created_at', 'updated_at', 'reviewed_at'
        ]


class ReviewRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating review requests."""

    class Meta:
        model = ReviewRequest
        fields = ['product_name', 'receipt_data']

    def create(self, validated_data):
        """Create review request for current user."""
        user = self.context['request'].user
        return ReviewRequest.objects.create(
            user=user,
            **validated_data
        )


class ReviewRequestActionSerializer(serializers.Serializer):
    """Serializer for admin actions on review requests."""

    admin_comment = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional comment from admin"
    )
    points_awarded = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        help_text="Points to award (only for approval)"
    )


class ReviewRequestStatsSerializer(serializers.Serializer):
    """Serializer for review request statistics."""

    total = serializers.IntegerField()
    pending = serializers.IntegerField()
    approved = serializers.IntegerField()
    rejected = serializers.IntegerField()
