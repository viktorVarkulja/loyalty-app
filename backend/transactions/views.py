from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django.utils import timezone

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


@extend_schema(
    summary="Request review for unmatched product",
    description="Request admin review for a product that wasn't matched in the system.",
    request={
        'type': 'object',
        'properties': {
            'notes': {'type': 'string', 'description': 'Optional notes from user about the product'}
        }
    },
    responses={
        200: {'description': 'Review requested successfully'},
        400: {'description': 'Item already matched or already under review'},
        404: {'description': 'Transaction item not found'}
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_item_review(request, item_id):
    """Request admin review for an unmatched product."""
    try:
        # Get the item and verify it belongs to user's transaction
        item = TransactionItem.objects.select_related('transaction').get(
            id=item_id,
            transaction__user=request.user
        )
    except TransactionItem.DoesNotExist:
        return Response(
            {'error': 'Transaction item not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if item is already matched
    if item.matched:
        return Response(
            {'error': 'This product is already matched'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if already under review
    if item.review_status in ['pending', 'approved']:
        return Response(
            {'error': f'This product is already {item.review_status}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update item status to pending review
    item.review_status = 'pending'
    item.review_requested_at = timezone.now()
    item.review_notes = request.data.get('notes', '')
    item.save()

    return Response({
        'success': True,
        'message': 'Review request submitted successfully',
        'item': TransactionItemSerializer(item).data
    })


@extend_schema(
    summary="Get pending review items (Admin only)",
    description="Get list of all products pending admin review.",
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_pending_reviews(request):
    """Get all items pending review (admin only)."""
    items = TransactionItem.objects.filter(
        review_status='pending'
    ).select_related('transaction__user', 'transaction__store').order_by('-review_requested_at')

    # Serialize with additional user info
    items_data = []
    for item in items:
        item_data = TransactionItemSerializer(item).data
        item_data['user'] = {
            'id': item.transaction.user.id,
            'email': item.transaction.user.email
        }
        item_data['store'] = {
            'name': item.transaction.store.name,
            'location': item.transaction.store.location
        }
        item_data['scanned_at'] = item.transaction.scanned_at
        items_data.append(item_data)

    return Response({
        'count': len(items_data),
        'items': items_data
    })


@extend_schema(
    summary="Approve review and assign points (Admin only)",
    description="Approve a product review and assign points to the user.",
    request={
        'type': 'object',
        'properties': {
            'product_id': {'type': 'string', 'description': 'ID of matching product'},
            'points': {'type': 'integer', 'description': 'Points to award'},
            'notes': {'type': 'string', 'description': 'Admin notes'}
        },
        'required': ['points']
    }
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_review(request, item_id):
    """Approve a review and assign points (admin only)."""
    try:
        item = TransactionItem.objects.select_related('transaction__user').get(id=item_id)
    except TransactionItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    if item.review_status != 'pending':
        return Response(
            {'error': 'Item is not pending review'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get points from request
    points = request.data.get('points', 0)
    product_id = request.data.get('product_id')
    admin_notes = request.data.get('notes', '')

    print(f"🔍 DEBUG approve_review - Item: {item.product_name}")
    print(f"🔍 DEBUG approve_review - Points: {points}")
    print(f"🔍 DEBUG approve_review - product_id from request: {product_id}")
    print(f"🔍 DEBUG approve_review - item.product (existing): {item.product}")

    # Create or get product in the database
    from products.models import Product

    if product_id:
        print(f"✅ Branch 1: product_id provided = {product_id}")

        # Admin specified an existing product
        item.product_id = product_id
    elif not item.product:
        print(f"✅ Branch 2: No product linked, creating new product")
        # Create a new product entry if not already linked
        product, created = Product.objects.get_or_create(
            name=item.product_name,
            defaults={
                'points': points,
                'status': 'ACTIVE'
            }
        )
        print(f"🔍 Product created: {product.name}, Created new? {created}, ID: {product.id}")
        item.product = product
    else:
        print(f"⚠️ Branch 3: Product already linked - {item.product}")

    # Update item
    item.review_status = 'approved'
    item.matched = True  # Mark as matched when approved
    item.points = points
    item.review_notes = admin_notes
    item.save()

    # Update user points
    user = item.transaction.user
    user.points += points
    user.save()

    # Update transaction total points
    transaction = item.transaction
    transaction.total_points += points
    transaction.save()

    return Response({
        'success': True,
        'message': f'Review approved. Product created/linked and {points} points awarded to user.',
        'item': TransactionItemSerializer(item).data
    })


@extend_schema(
    summary="Reject review (Admin only)",
    description="Reject a product review request.",
    request={
        'type': 'object',
        'properties': {
            'notes': {'type': 'string', 'description': 'Reason for rejection'}
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_review(request, item_id):
    """Reject a review request (admin only)."""
    try:
        item = TransactionItem.objects.get(id=item_id)
    except TransactionItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    if item.review_status != 'pending':
        return Response(
            {'error': 'Item is not pending review'},
            status=status.HTTP_400_BAD_REQUEST
        )

    admin_notes = request.data.get('notes', 'Rejected by admin')
    item.review_status = 'rejected'
    item.review_notes = admin_notes
    item.save()

    return Response({
        'success': True,
        'message': 'Review rejected',
        'item': TransactionItemSerializer(item).data
    })
