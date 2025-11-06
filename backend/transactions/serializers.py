from rest_framework import serializers
from .models import Transaction, TransactionItem
from products.serializers import StoreSerializer


class TransactionItemSerializer(serializers.ModelSerializer):
    """Serializer for TransactionItem model."""

    class Meta:
        model = TransactionItem
        fields = [
            'id', 'product_id', 'product_name', 'quantity',
            'price', 'unit_price', 'points', 'matched'
        ]
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""

    items = TransactionItemSerializer(many=True, read_only=True)
    store = StoreSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'store', 'total_points', 'total_amount', 'receipt_url',
            'receipt_data', 'scanned_at', 'created_at', 'items'
        ]
        read_only_fields = ['id', 'scanned_at', 'created_at']


class ReceiptScanSerializer(serializers.Serializer):
    """Serializer for receipt scanning input."""

    qr_data = serializers.CharField(
        required=True,
        help_text="QR code data from fiscal receipt (URL or raw QR string)"
    )


class ReceiptScanResponseSerializer(serializers.Serializer):
    """Serializer for receipt scanning response."""

    success = serializers.BooleanField()
    transaction_id = serializers.CharField(required=False)
    store = serializers.DictField(required=False)
    total_points = serializers.IntegerField(required=False)
    items = serializers.ListField(required=False)
    unmatched_items = serializers.ListField(required=False)
    error = serializers.CharField(required=False)
