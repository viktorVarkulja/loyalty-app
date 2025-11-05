from django.db import models
from django.conf import settings
import secrets
import time


def generate_cuid():
    """Generate a cuid-like ID."""
    timestamp = int(time.time() * 1000)
    random_part = secrets.token_urlsafe(16)[:16]
    return f"c{timestamp}{random_part}"


class ReviewRequest(models.Model):
    """Review Request model for unknown products matching Prisma schema."""

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_requests',
        db_index=True,
        db_column='userId'
    )
    product_name = models.CharField(max_length=255, db_column='productName')
    receipt_data = models.JSONField(null=True, blank=True, db_column='receiptData')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        db_index=True
    )
    admin_comment = models.TextField(null=True, blank=True, db_column='adminComment')
    points_awarded = models.IntegerField(default=0, db_column='pointsAwarded')
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')
    reviewed_at = models.DateTimeField(null=True, blank=True, db_column='reviewedAt')

    class Meta:
        db_table = 'review_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Review: {self.product_name} - {self.status}"
