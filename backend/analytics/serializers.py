"""
Serializers for Analytics API endpoints.
"""

from rest_framework import serializers
from .models import (
    StoreAnalytics,
    ProductAnalytics,
    UserActivityLog,
    StoreProductRanking,
    UserStoreActivity
)


class StoreAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for Store Analytics."""

    store_name = serializers.CharField(source='store.name', read_only=True)
    store_location = serializers.CharField(source='store.location', read_only=True)

    class Meta:
        model = StoreAnalytics
        fields = [
            'id',
            'store_name',
            'store_location',
            'total_scans',
            'total_points_earned',
            'total_points_redeemed',
            'unique_users',
            'total_revenue',
            'last_updated'
        ]


class ProductAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for Product Analytics."""

    product_name = serializers.CharField(source='product.name', read_only=True)
    product_points = serializers.IntegerField(source='product.points', read_only=True)

    class Meta:
        model = ProductAnalytics
        fields = [
            'id',
            'product_name',
            'product_points',
            'total_scans',
            'total_quantity',
            'total_revenue',
            'unique_users',
            'last_updated'
        ]


class UserActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for User Activity Logs."""

    class Meta:
        model = UserActivityLog
        fields = [
            'id',
            'date',
            'total_scans',
            'total_points_earned',
            'total_points_redeemed',
            'active_users',
            'new_users',
            'new_products_scanned',
            'created_at'
        ]


class StoreProductRankingSerializer(serializers.ModelSerializer):
    """Serializer for Store Product Rankings."""

    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = StoreProductRanking
        fields = [
            'id',
            'store_name',
            'product_name',
            'scan_count',
            'total_quantity',
            'total_revenue',
            'last_updated'
        ]


class UserStoreActivitySerializer(serializers.ModelSerializer):
    """Serializer for User Store Activities."""

    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = UserStoreActivity
        fields = [
            'id',
            'user_email',
            'user_name',
            'store_name',
            'scan_count',
            'total_points_earned',
            'total_spent',
            'first_scan',
            'last_scan',
            'last_updated'
        ]
