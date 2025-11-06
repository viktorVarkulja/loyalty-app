from django.db import models
from django.conf import settings
from products.models import Store, Product
import secrets
import time


def generate_cuid():
    """Generate a cuid-like ID."""
    timestamp = int(time.time() * 1000)
    random_part = secrets.token_urlsafe(16)[:16]
    return f"c{timestamp}{random_part}"


class Transaction(models.Model):
    """Transaction model (purchase/scan history) matching Prisma schema."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        db_index=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name='transactions',
        db_index=True
    )
    total_points = models.IntegerField()
    receipt_url = models.URLField(max_length=500, null=True, blank=True)
    receipt_data = models.JSONField(null=True, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-scanned_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['store']),
            models.Index(fields=['scanned_at']),
        ]

    def __str__(self):
        return f"Transaction {self.id[:8]} - {self.user.email} - {self.total_points} points"


class TransactionItem(models.Model):
    """Individual products in a receipt matching Prisma schema."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='transaction_items',
        null=True,
        blank=True
    )
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(null=True, blank=True)
    points = models.IntegerField(default=0)
    matched = models.BooleanField(default=False)

    class Meta:
        db_table = 'transaction_items'
        ordering = ['id']
        indexes = [
            models.Index(fields=['transaction']),
        ]

    def __str__(self):
        return f"{self.product_name} x{self.quantity} ({self.points} points)"
