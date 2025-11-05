from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Transaction, TransactionItem
from .serializers import (
    TransactionSerializer,
    TransactionItemSerializer,
    ReceiptScanSerializer,
    ReceiptScanResponseSerializer
)
from .services import ReceiptProcessingService


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing transaction history."""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return transactions for the current user."""
        return Transaction.objects.filter(user=self.request.user).select_related('store').prefetch_related('items')

    @extend_schema(
        summary="List user's transaction history",
        description="Get all transactions (receipt scans) for the authenticated user.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get transaction details",
        description="Retrieve details of a specific transaction including all items.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(
    summary="Scan fiscal receipt QR code",
    description="""
    Process a Serbian fiscal receipt by scanning its QR code.

    The endpoint will:
    1. Extract the receipt URL from QR code data
    2. Fetch receipt data from Serbian Tax Authority (SUF) system
    3. Parse receipt items and match them with products in database
    4. Calculate points for matched products
    5. Create transaction record
    6. Update user's points balance

    Returns transaction details with matched/unmatched items.
    """,
    request=ReceiptScanSerializer,
    responses={
        200: ReceiptScanResponseSerializer,
        400: OpenApiResponse(description="Invalid QR data or processing error"),
        401: OpenApiResponse(description="Not authenticated")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scan_receipt(request):
    """Process receipt QR code and award points."""
    serializer = ReceiptScanSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    qr_data = serializer.validated_data['qr_data']

    # Process receipt using service
    result = ReceiptProcessingService.process_receipt(qr_data, request.user)

    if not result['success']:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    return Response(result, status=status.HTTP_200_OK)


@extend_schema(
    summary="Get user's points balance",
    description="Get the current points balance for the authenticated user.",
    responses={
        200: {
            'type': 'object',
            'properties': {
                'points': {'type': 'integer'},
                'user_id': {'type': 'string'},
                'email': {'type': 'string'}
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_points_balance(request):
    """Get user's current points balance."""
    return Response({
        'points': request.user.points,
        'user_id': request.user.id,
        'email': request.user.email
    })
