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


class StoreAnalytics(models.Model):
    """Aggregated analytics for stores - updated periodically for performance."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    store = models.OneToOneField(
        Store,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    total_scans = models.IntegerField(default=0, help_text="Total number of receipt scans")
    total_points_earned = models.IntegerField(default=0, help_text="Total points earned by all users")
    total_points_redeemed = models.IntegerField(default=0, help_text="Total points redeemed/used")
    unique_users = models.IntegerField(default=0, help_text="Unique users who scanned receipts")
    total_revenue = models.FloatField(default=0.0, help_text="Total revenue in RSD")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'store_analytics'
        verbose_name = 'Store Analytics'
        verbose_name_plural = 'Store Analytics'
        ordering = ['-total_scans']

    def __str__(self):
        return f"{self.store.name} Analytics"


class ProductAnalytics(models.Model):
    """Aggregated analytics for products."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    total_scans = models.IntegerField(default=0, help_text="Total times this product was scanned")
    total_quantity = models.IntegerField(default=0, help_text="Total quantity purchased")
    total_revenue = models.FloatField(default=0.0, help_text="Total revenue generated in RSD")
    unique_users = models.IntegerField(default=0, help_text="Unique users who purchased")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_analytics'
        verbose_name = 'Product Analytics'
        verbose_name_plural = 'Product Analytics'
        ordering = ['-total_scans']

    def __str__(self):
        return f"{self.product.name} Analytics"


class UserActivityLog(models.Model):
    """Daily aggregated user activity for trend analysis."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    date = models.DateField(db_index=True, help_text="Date of activity")
    total_scans = models.IntegerField(default=0, help_text="Total scans on this date")
    total_points_earned = models.IntegerField(default=0, help_text="Total points earned")
    total_points_redeemed = models.IntegerField(default=0, help_text="Total points redeemed")
    active_users = models.IntegerField(default=0, help_text="Number of active users")
    new_users = models.IntegerField(default=0, help_text="Number of new registrations")
    new_products_scanned = models.IntegerField(default=0, help_text="New unique products scanned")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activity_logs'
        verbose_name = 'User Activity Log'
        verbose_name_plural = 'User Activity Logs'
        ordering = ['-date']
        unique_together = ['date']
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"Activity for {self.date}"


class StoreProductRanking(models.Model):
    """Track top products per store - updated periodically."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='product_rankings'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='store_rankings',
        null=True,
        blank=True
    )
    product_name = models.CharField(max_length=255, help_text="Product name for unmatched items")
    scan_count = models.IntegerField(default=0, help_text="Number of times scanned")
    total_quantity = models.IntegerField(default=0, help_text="Total quantity purchased")
    total_revenue = models.FloatField(default=0.0, help_text="Total revenue in RSD")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'store_product_rankings'
        verbose_name = 'Store Product Ranking'
        verbose_name_plural = 'Store Product Rankings'
        ordering = ['store', '-scan_count']
        unique_together = ['store', 'product_name']
        indexes = [
            models.Index(fields=['store', '-scan_count']),
        ]

    def __str__(self):
        return f"{self.store.name} - {self.product_name} ({self.scan_count} scans)"


class UserStoreActivity(models.Model):
    """Track user activity per store for repeat customer analysis."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='store_activities'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='user_activities'
    )
    scan_count = models.IntegerField(default=0, help_text="Number of scans by this user")
    total_points_earned = models.IntegerField(default=0, help_text="Total points earned")
    total_spent = models.FloatField(default=0.0, help_text="Total amount spent in RSD")
    first_scan = models.DateTimeField(null=True, blank=True)
    last_scan = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_store_activities'
        verbose_name = 'User Store Activity'
        verbose_name_plural = 'User Store Activities'
        ordering = ['store', '-scan_count']
        unique_together = ['user', 'store']
        indexes = [
            models.Index(fields=['store', '-scan_count']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.store.name} ({self.scan_count} scans)"
