from django.db import models
from django.conf import settings
import secrets
import time


def generate_cuid():
    """Generate a cuid-like ID."""
    timestamp = int(time.time() * 1000)
    random_part = secrets.token_urlsafe(16)[:16]
    return f"c{timestamp}{random_part}"


class Store(models.Model):
    """Store model matching Prisma schema."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        db_table = 'stores'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model matching Prisma schema."""

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    points = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        db_table = 'products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.points} points)"


class UserFavoriteStore(models.Model):
    """Many-to-many relationship between users and favorite stores."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_stores',
        db_column='userId'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='favorited_by_users',
        db_column='storeId'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'user_favorite_stores'
        unique_together = ['user', 'store']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.store.name}"


class ApiKey(models.Model):
    """API Keys for webshop integration."""

    id = models.CharField(max_length=30, primary_key=True, default=generate_cuid, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_keys',
        db_column='userId'
    )
    key = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    last_used = models.DateTimeField(null=True, blank=True, db_column='lastUsed')

    class Meta:
        db_table = 'api_keys'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    def save(self, *args, **kwargs):
        """Generate API key if not exists."""
        if not self.key:
            self.key = f"loy_{secrets.token_urlsafe(32)}"
        super().save(*args, **kwargs)
