from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import ReviewRequest
from .serializers import (
    ReviewRequestSerializer,
    ReviewRequestCreateSerializer,
    ReviewRequestActionSerializer,
    ReviewRequestStatsSerializer
)


class ReviewRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for ReviewRequest CRUD operations."""

    serializer_class = ReviewRequestSerializer

    def get_permissions(self):
        """
        Admin can view all and perform actions.
        Regular users can only create and view their own.
        """
        if self.action in ['approve', 'reject', 'list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Admin sees all requests.
        Regular users see only their own.
        """
        if self.request.user.role == 'ADMIN':
            return ReviewRequest.objects.all().select_related('user')
        return ReviewRequest.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Use different serializer for create action."""
        if self.action == 'create':
            return ReviewRequestCreateSerializer
        return ReviewRequestSerializer

    @extend_schema(
        summary="List review requests",
        description="Admin: See all review requests. User: See only their own.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get review request details",
        description="Get details of a specific review request.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Submit product for review",
        description="User submits an unknown product for admin review.",
        request=ReviewRequestCreateSerializer,
        responses={201: ReviewRequestSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review_request = serializer.save()

        # Return full serializer
        output_serializer = ReviewRequestSerializer(review_request)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Approve review request (Admin only)",
        description="Admin approves a review request and awards points to the user.",
        request=ReviewRequestActionSerializer,
        responses={
            200: ReviewRequestSerializer,
            400: OpenApiResponse(description="Invalid request"),
            404: OpenApiResponse(description="Review request not found")
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """Admin approves a review request and awards points."""
        review_request = self.get_object()

        if review_request.status != 'PENDING':
            return Response(
                {"detail": "Only pending requests can be approved."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        points_awarded = serializer.validated_data.get('points_awarded', 0)
        admin_comment = serializer.validated_data.get('admin_comment', '')

        # Update review request
        review_request.status = 'APPROVED'
        review_request.points_awarded = points_awarded
        review_request.admin_comment = admin_comment
        review_request.reviewed_at = timezone.now()
        review_request.save()

        # Award points to user
        if points_awarded > 0:
            user = review_request.user
            user.points += points_awarded
            user.save()

        output_serializer = ReviewRequestSerializer(review_request)
        return Response(output_serializer.data)

    @extend_schema(
        summary="Reject review request (Admin only)",
        description="Admin rejects a review request with optional comment.",
        request=ReviewRequestActionSerializer,
        responses={
            200: ReviewRequestSerializer,
            400: OpenApiResponse(description="Invalid request"),
            404: OpenApiResponse(description="Review request not found")
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """Admin rejects a review request."""
        review_request = self.get_object()

        if review_request.status != 'PENDING':
            return Response(
                {"detail": "Only pending requests can be rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        admin_comment = serializer.validated_data.get('admin_comment', '')

        # Update review request
        review_request.status = 'REJECTED'
        review_request.admin_comment = admin_comment
        review_request.reviewed_at = timezone.now()
        review_request.save()

        output_serializer = ReviewRequestSerializer(review_request)
        return Response(output_serializer.data)

    @extend_schema(
        summary="Get review request statistics (Admin only)",
        description="Get statistics about review requests (total, pending, approved, rejected).",
        responses={200: ReviewRequestStatsSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def stats(self, request):
        """Get statistics about review requests."""
        stats = ReviewRequest.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            approved=Count('id', filter=Q(status='APPROVED')),
            rejected=Count('id', filter=Q(status='REJECTED'))
        )

        serializer = ReviewRequestStatsSerializer(stats)
        return Response(serializer.data)


@extend_schema(
    summary="Get user's review requests",
    description="Get all review requests submitted by the authenticated user.",
    responses={200: ReviewRequestSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_review_requests(request):
    """Get current user's review requests."""
    reviews = ReviewRequest.objects.filter(user=request.user)
    serializer = ReviewRequestSerializer(reviews, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Get pending review requests (Admin only)",
    description="Get all pending review requests that need admin attention.",
    responses={200: ReviewRequestSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def pending_reviews(request):
    """Get all pending review requests for admin."""
    reviews = ReviewRequest.objects.filter(status='PENDING').select_related('user')
    serializer = ReviewRequestSerializer(reviews, many=True)
    return Response(serializer.data)
