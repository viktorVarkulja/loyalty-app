"""
Analytics service for computing statistics with optimized queries.
This service uses Django ORM aggregations and annotations for efficient data retrieval.
"""

from django.db.models import Count, Sum, Q, F, Max, Min, Avg
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

from products.models import Store, Product
from transactions.models import Transaction, TransactionItem
from users.models import User
from .models import (
    StoreAnalytics,
    ProductAnalytics,
    UserActivityLog,
    StoreProductRanking,
    UserStoreActivity
)


class AnalyticsService:
    """Service class for computing and retrieving analytics data."""

    # ==================== PRODUCT & STORE ANALYTICS ====================

    @staticmethod
    def get_most_scanned_products_by_store(store_id=None, limit=10):
        """
        Get most scanned products for a specific store or all stores.
        Returns optimized queryset with product info and scan counts.
        """
        queryset = TransactionItem.objects.filter(matched=True)

        if store_id:
            queryset = queryset.filter(transaction__store_id=store_id)

        # Group by product and aggregate
        results = queryset.values(
            'product_id',
            'product__name',
            'transaction__store__name'
        ).annotate(
            scan_count=Count('id'),
            total_quantity=Sum('quantity'),
            total_revenue=Sum('price'),
            unique_users=Count('transaction__user', distinct=True)
        ).order_by('-scan_count')[:limit]

        return list(results)

    @staticmethod
    def get_store_rankings_by_scans(limit=10):
        """
        Get stores ranked by total number of scans.
        """
        results = Transaction.objects.values(
            'store_id',
            'store__name',
            'store__location'
        ).annotate(
            total_scans=Count('id'),
            unique_users=Count('user', distinct=True),
            total_points=Sum('total_points'),
            total_revenue=Sum('total_amount')
        ).order_by('-total_scans')[:limit]

        return list(results)

    @staticmethod
    def get_store_rankings_by_points(limit=10):
        """
        Get stores ranked by total points earned (redemption activity).
        """
        results = Transaction.objects.values(
            'store_id',
            'store__name',
            'store__location'
        ).annotate(
            total_scans=Count('id'),
            total_points_earned=Sum('total_points'),
            unique_users=Count('user', distinct=True)
        ).order_by('-total_points_earned')[:limit]

        return list(results)

    # ==================== USER ACTIVITY TRENDS ====================

    @staticmethod
    def get_weekly_activity_trend(weeks=12):
        """
        Get weekly user activity trend for the last N weeks.
        """
        start_date = timezone.now() - timedelta(weeks=weeks)

        weekly_data = Transaction.objects.filter(
            scanned_at__gte=start_date
        ).annotate(
            week=TruncWeek('scanned_at')
        ).values('week').annotate(
            total_scans=Count('id'),
            active_users=Count('user', distinct=True),
            total_points=Sum('total_points'),
            total_revenue=Sum('total_amount')
        ).order_by('week')

        return list(weekly_data)

    @staticmethod
    def get_monthly_activity_trend(months=12):
        """
        Get monthly user activity trend for the last N months.
        """
        start_date = timezone.now() - timedelta(days=months*30)

        monthly_data = Transaction.objects.filter(
            scanned_at__gte=start_date
        ).annotate(
            month=TruncMonth('scanned_at')
        ).values('month').annotate(
            total_scans=Count('id'),
            active_users=Count('user', distinct=True),
            total_points=Sum('total_points'),
            total_revenue=Sum('total_amount')
        ).order_by('month')

        return list(monthly_data)

    @staticmethod
    def get_daily_activity_trend(days=30):
        """
        Get daily user activity trend for the last N days.
        """
        start_date = timezone.now() - timedelta(days=days)

        daily_data = Transaction.objects.filter(
            scanned_at__gte=start_date
        ).annotate(
            date=TruncDate('scanned_at')
        ).values('date').annotate(
            total_scans=Count('id'),
            active_users=Count('user', distinct=True),
            total_points=Sum('total_points'),
            total_revenue=Sum('total_amount')
        ).order_by('date')

        return list(daily_data)

    @staticmethod
    def get_new_products_growth(days=30):
        """
        Track growth of new unique products being scanned over time.
        """
        start_date = timezone.now() - timedelta(days=days)

        # Get products with their first scan date
        product_growth = TransactionItem.objects.filter(
            matched=True,
            transaction__scanned_at__gte=start_date
        ).values(
            'product_id',
            'product__name'
        ).annotate(
            first_scan=Min('transaction__scanned_at'),
            total_scans=Count('id')
        ).order_by('first_scan')

        return list(product_growth)

    # ==================== STORE-SPECIFIC REPORTS ====================

    @staticmethod
    def get_store_detailed_report(store_id, days=30):
        """
        Get comprehensive report for a specific store.
        """
        start_date = timezone.now() - timedelta(days=days)

        # Basic store stats
        store_stats = Transaction.objects.filter(
            store_id=store_id,
            scanned_at__gte=start_date
        ).aggregate(
            total_scans=Count('id'),
            unique_users=Count('user', distinct=True),
            total_points_earned=Sum('total_points'),
            total_revenue=Sum('total_amount'),
            avg_transaction_value=Avg('total_amount')
        )

        # Top products
        top_products = AnalyticsService.get_most_scanned_products_by_store(
            store_id=store_id,
            limit=10
        )

        # Top repeat customers
        top_customers = AnalyticsService.get_top_repeat_customers(
            store_id=store_id,
            limit=10
        )

        # Points usage stats
        points_stats = AnalyticsService.get_store_points_stats(store_id)

        return {
            'store_stats': store_stats,
            'top_products': top_products,
            'top_customers': top_customers,
            'points_stats': points_stats
        }

    @staticmethod
    def get_top_repeat_customers(store_id, limit=10):
        """
        Get users who return most often to a specific store.
        """
        repeat_customers = Transaction.objects.filter(
            store_id=store_id
        ).values(
            'user_id',
            'user__email',
            'user__name'
        ).annotate(
            scan_count=Count('id'),
            total_points_earned=Sum('total_points'),
            total_spent=Sum('total_amount'),
            first_visit=Min('scanned_at'),
            last_visit=Max('scanned_at')
        ).order_by('-scan_count')[:limit]

        return list(repeat_customers)

    @staticmethod
    def get_store_points_stats(store_id):
        """
        Get points earned vs redeemed statistics for a store.
        Note: Points redemption tracking would require additional models/tracking.
        Currently showing earned points.
        """
        stats = Transaction.objects.filter(
            store_id=store_id
        ).aggregate(
            total_points_earned=Sum('total_points'),
            avg_points_per_transaction=Avg('total_points'),
            max_points_transaction=Max('total_points'),
            min_points_transaction=Min('total_points')
        )

        return stats

    # ==================== ADDITIONAL METRICS ====================

    @staticmethod
    def get_new_product_scan_frequency(days=30):
        """
        Get frequency of new products being scanned (products scanned for first time).
        """
        start_date = timezone.now() - timedelta(days=days)

        # Get products that were first scanned in the date range
        new_products = TransactionItem.objects.filter(
            matched=True
        ).values('product_id').annotate(
            first_scan=Min('transaction__scanned_at')
        ).filter(
            first_scan__gte=start_date
        ).annotate(
            date=TruncDate('first_scan')
        ).values('date').annotate(
            new_product_count=Count('product_id', distinct=True)
        ).order_by('date')

        return list(new_products)

    @staticmethod
    def get_user_leaderboard(limit=20):
        """
        Get top users by points earned.
        """
        leaderboard = User.objects.annotate(
            total_scans=Count('transactions'),
            total_points_earned=Sum('transactions__total_points')
        ).order_by('-points', '-total_scans')[:limit]

        return [{
            'user_id': user.id,
            'email': user.email,
            'name': user.name,
            'current_points': user.points,
            'total_scans': user.total_scans,
            'total_points_earned': user.total_points_earned or 0
        } for user in leaderboard]

    @staticmethod
    def get_store_leaderboard(limit=20):
        """
        Get comprehensive store leaderboard.
        """
        stores = Store.objects.annotate(
            total_scans=Count('transactions'),
            unique_customers=Count('transactions__user', distinct=True),
            total_points_distributed=Sum('transactions__total_points'),
            total_revenue=Sum('transactions__total_amount')
        ).order_by('-total_scans')[:limit]

        return [{
            'store_id': store.id,
            'name': store.name,
            'location': store.location,
            'total_scans': store.total_scans,
            'unique_customers': store.unique_customers,
            'total_points_distributed': store.total_points_distributed or 0,
            'total_revenue': store.total_revenue or 0.0
        } for store in stores]

    @staticmethod
    def get_product_leaderboard(limit=20):
        """
        Get top products by scan count.
        """
        products = TransactionItem.objects.filter(
            matched=True
        ).values(
            'product_id',
            'product__name',
            'product__points'
        ).annotate(
            scan_count=Count('id'),
            total_quantity=Sum('quantity'),
            total_revenue=Sum('price'),
            unique_users=Count('transaction__user', distinct=True)
        ).order_by('-scan_count')[:limit]

        return list(products)

    # ==================== CACHE UPDATE METHODS ====================

    @staticmethod
    def update_store_analytics(store_id=None):
        """
        Update cached store analytics. Can update specific store or all stores.
        """
        if store_id:
            stores = Store.objects.filter(id=store_id)
        else:
            stores = Store.objects.all()

        for store in stores:
            # Get aggregated data
            stats = Transaction.objects.filter(store=store).aggregate(
                total_scans=Count('id'),
                total_points_earned=Sum('total_points'),
                unique_users=Count('user', distinct=True),
                total_revenue=Sum('total_amount')
            )

            # Update or create analytics record
            StoreAnalytics.objects.update_or_create(
                store=store,
                defaults={
                    'total_scans': stats['total_scans'] or 0,
                    'total_points_earned': stats['total_points_earned'] or 0,
                    'unique_users': stats['unique_users'] or 0,
                    'total_revenue': stats['total_revenue'] or 0.0,
                    'total_points_redeemed': 0  # To be implemented with redemption tracking
                }
            )

    @staticmethod
    def update_product_analytics(product_id=None):
        """
        Update cached product analytics. Can update specific product or all products.
        """
        if product_id:
            products = Product.objects.filter(id=product_id)
        else:
            products = Product.objects.all()

        for product in products:
            # Get aggregated data
            stats = TransactionItem.objects.filter(
                product=product,
                matched=True
            ).aggregate(
                total_scans=Count('id'),
                total_quantity=Sum('quantity'),
                total_revenue=Sum('price'),
                unique_users=Count('transaction__user', distinct=True)
            )

            # Update or create analytics record
            ProductAnalytics.objects.update_or_create(
                product=product,
                defaults={
                    'total_scans': stats['total_scans'] or 0,
                    'total_quantity': stats['total_quantity'] or 0,
                    'total_revenue': stats['total_revenue'] or 0.0,
                    'unique_users': stats['unique_users'] or 0
                }
            )

    @staticmethod
    def update_store_product_rankings(store_id=None):
        """
        Update store-product ranking cache.
        """
        if store_id:
            stores = Store.objects.filter(id=store_id)
        else:
            stores = Store.objects.all()

        for store in stores:
            # Get product rankings for this store
            rankings = TransactionItem.objects.filter(
                transaction__store=store
            ).values('product_name', 'product_id').annotate(
                scan_count=Count('id'),
                total_quantity=Sum('quantity'),
                total_revenue=Sum('price')
            ).order_by('-scan_count')

            # Clear old rankings for this store
            StoreProductRanking.objects.filter(store=store).delete()

            # Create new rankings
            for rank in rankings:
                StoreProductRanking.objects.create(
                    store=store,
                    product_id=rank['product_id'],
                    product_name=rank['product_name'],
                    scan_count=rank['scan_count'],
                    total_quantity=rank['total_quantity'],
                    total_revenue=rank['total_revenue'] or 0.0
                )

    @staticmethod
    def update_user_store_activities():
        """
        Update user-store activity cache for repeat customer analysis.
        """
        # Get all user-store combinations with activity
        activities = Transaction.objects.values(
            'user_id', 'store_id'
        ).annotate(
            scan_count=Count('id'),
            total_points_earned=Sum('total_points'),
            total_spent=Sum('total_amount'),
            first_scan=Min('scanned_at'),
            last_scan=Max('scanned_at')
        )

        # Clear old data
        UserStoreActivity.objects.all().delete()

        # Create new records
        for activity in activities:
            UserStoreActivity.objects.create(
                user_id=activity['user_id'],
                store_id=activity['store_id'],
                scan_count=activity['scan_count'],
                total_points_earned=activity['total_points_earned'] or 0,
                total_spent=activity['total_spent'] or 0.0,
                first_scan=activity['first_scan'],
                last_scan=activity['last_scan']
            )

    @staticmethod
    def update_all_analytics():
        """
        Update all cached analytics data. Should be run periodically (e.g., daily cron job).
        """
        print("Updating store analytics...")
        AnalyticsService.update_store_analytics()

        print("Updating product analytics...")
        AnalyticsService.update_product_analytics()

        print("Updating store-product rankings...")
        AnalyticsService.update_store_product_rankings()

        print("Updating user-store activities...")
        AnalyticsService.update_user_store_activities()

        print("Analytics update complete!")
