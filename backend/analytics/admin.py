from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum
from datetime import datetime, timedelta
import csv

from .models import (
    StoreAnalytics,
    ProductAnalytics,
    UserActivityLog,
    StoreProductRanking,
    UserStoreActivity
)
from .services import AnalyticsService


class AnalyticsDashboardAdmin(admin.ModelAdmin):
    """
    Custom admin view for Analytics Dashboard.
    This provides a central place to view all statistics.
    """
    change_list_template = 'admin/analytics_dashboard.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Get time range from request (default: last 30 days)
        days = int(request.GET.get('days', 30))

        # Fetch key metrics
        extra_context['store_rankings'] = AnalyticsService.get_store_rankings_by_scans(limit=10)
        extra_context['user_leaderboard'] = AnalyticsService.get_user_leaderboard(limit=10)
        extra_context['product_leaderboard'] = AnalyticsService.get_product_leaderboard(limit=10)
        extra_context['weekly_trend'] = AnalyticsService.get_weekly_activity_trend(weeks=12)
        extra_context['monthly_trend'] = AnalyticsService.get_monthly_activity_trend(months=6)
        extra_context['selected_days'] = days

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(StoreAnalytics)
class StoreAnalyticsAdmin(admin.ModelAdmin):
    """Admin interface for Store Analytics."""

    list_display = [
        'store_name',
        'total_scans',
        'unique_users',
        'total_points_earned',
        'total_revenue_display',
        'last_updated'
    ]
    list_filter = ['last_updated']
    search_fields = ['store__name', 'store__location']
    readonly_fields = [
        'store',
        'total_scans',
        'total_points_earned',
        'total_points_redeemed',
        'unique_users',
        'total_revenue',
        'last_updated'
    ]
    ordering = ['-total_scans']
    actions = ['refresh_analytics', 'export_to_csv']

    def store_name(self, obj):
        return obj.store.name
    store_name.short_description = 'Store'
    store_name.admin_order_field = 'store__name'

    def total_revenue_display(self, obj):
        return f"{obj.total_revenue:,.2f} RSD"
    total_revenue_display.short_description = 'Total Revenue'
    total_revenue_display.admin_order_field = 'total_revenue'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def refresh_analytics(self, request, queryset):
        """Refresh analytics for selected stores."""
        for analytics in queryset:
            AnalyticsService.update_store_analytics(store_id=analytics.store.id)
        self.message_user(request, f"Analytics refreshed for {queryset.count()} store(s).")
    refresh_analytics.short_description = "Refresh selected store analytics"

    def export_to_csv(self, request, queryset):
        """Export selected analytics to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="store_analytics.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Store', 'Location', 'Total Scans', 'Unique Users',
            'Points Earned', 'Points Redeemed', 'Revenue (RSD)', 'Last Updated'
        ])

        for obj in queryset:
            writer.writerow([
                obj.store.name,
                obj.store.location or '',
                obj.total_scans,
                obj.unique_users,
                obj.total_points_earned,
                obj.total_points_redeemed,
                obj.total_revenue,
                obj.last_updated.strftime('%Y-%m-%d %H:%M')
            ])

        return response
    export_to_csv.short_description = "Export to CSV"


@admin.register(ProductAnalytics)
class ProductAnalyticsAdmin(admin.ModelAdmin):
    """Admin interface for Product Analytics."""

    list_display = [
        'product_name',
        'total_scans',
        'total_quantity',
        'unique_users',
        'total_revenue_display',
        'last_updated'
    ]
    list_filter = ['last_updated']
    search_fields = ['product__name']
    readonly_fields = [
        'product',
        'total_scans',
        'total_quantity',
        'total_revenue',
        'unique_users',
        'last_updated'
    ]
    ordering = ['-total_scans']
    actions = ['refresh_analytics', 'export_to_csv']

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'
    product_name.admin_order_field = 'product__name'

    def total_revenue_display(self, obj):
        return f"{obj.total_revenue:,.2f} RSD"
    total_revenue_display.short_description = 'Total Revenue'
    total_revenue_display.admin_order_field = 'total_revenue'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def refresh_analytics(self, request, queryset):
        """Refresh analytics for selected products."""
        for analytics in queryset:
            AnalyticsService.update_product_analytics(product_id=analytics.product.id)
        self.message_user(request, f"Analytics refreshed for {queryset.count()} product(s).")
    refresh_analytics.short_description = "Refresh selected product analytics"

    def export_to_csv(self, request, queryset):
        """Export selected analytics to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="product_analytics.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Product', 'Total Scans', 'Total Quantity', 'Unique Users',
            'Revenue (RSD)', 'Last Updated'
        ])

        for obj in queryset:
            writer.writerow([
                obj.product.name,
                obj.total_scans,
                obj.total_quantity,
                obj.unique_users,
                obj.total_revenue,
                obj.last_updated.strftime('%Y-%m-%d %H:%M')
            ])

        return response
    export_to_csv.short_description = "Export to CSV"


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    """Admin interface for User Activity Logs."""

    list_display = [
        'date',
        'total_scans',
        'active_users',
        'new_users',
        'total_points_earned',
        'total_points_redeemed',
        'new_products_scanned'
    ]
    list_filter = ['date']
    date_hierarchy = 'date'
    readonly_fields = [
        'date',
        'total_scans',
        'total_points_earned',
        'total_points_redeemed',
        'active_users',
        'new_users',
        'new_products_scanned',
        'created_at'
    ]
    ordering = ['-date']
    actions = ['export_to_csv']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def export_to_csv(self, request, queryset):
        """Export activity logs to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_activity_logs.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Total Scans', 'Active Users', 'New Users',
            'Points Earned', 'Points Redeemed', 'New Products'
        ])

        for obj in queryset:
            writer.writerow([
                obj.date.strftime('%Y-%m-%d'),
                obj.total_scans,
                obj.active_users,
                obj.new_users,
                obj.total_points_earned,
                obj.total_points_redeemed,
                obj.new_products_scanned
            ])

        return response
    export_to_csv.short_description = "Export to CSV"


@admin.register(StoreProductRanking)
class StoreProductRankingAdmin(admin.ModelAdmin):
    """Admin interface for Store Product Rankings."""

    list_display = [
        'store_name',
        'product_name',
        'scan_count',
        'total_quantity',
        'total_revenue_display',
        'last_updated'
    ]
    list_filter = ['store', 'last_updated']
    search_fields = ['store__name', 'product_name']
    readonly_fields = [
        'store',
        'product',
        'product_name',
        'scan_count',
        'total_quantity',
        'total_revenue',
        'last_updated'
    ]
    ordering = ['store', '-scan_count']
    actions = ['refresh_rankings', 'export_to_csv']

    def store_name(self, obj):
        return obj.store.name
    store_name.short_description = 'Store'
    store_name.admin_order_field = 'store__name'

    def total_revenue_display(self, obj):
        return f"{obj.total_revenue:,.2f} RSD"
    total_revenue_display.short_description = 'Revenue'
    total_revenue_display.admin_order_field = 'total_revenue'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def refresh_rankings(self, request, queryset):
        """Refresh product rankings for stores."""
        store_ids = queryset.values_list('store_id', flat=True).distinct()
        for store_id in store_ids:
            AnalyticsService.update_store_product_rankings(store_id=store_id)
        self.message_user(request, f"Rankings refreshed for {len(store_ids)} store(s).")
    refresh_rankings.short_description = "Refresh product rankings"

    def export_to_csv(self, request, queryset):
        """Export rankings to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="store_product_rankings.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Store', 'Product', 'Scan Count', 'Total Quantity',
            'Revenue (RSD)', 'Last Updated'
        ])

        for obj in queryset:
            writer.writerow([
                obj.store.name,
                obj.product_name,
                obj.scan_count,
                obj.total_quantity,
                obj.total_revenue,
                obj.last_updated.strftime('%Y-%m-%d %H:%M')
            ])

        return response
    export_to_csv.short_description = "Export to CSV"


@admin.register(UserStoreActivity)
class UserStoreActivityAdmin(admin.ModelAdmin):
    """Admin interface for User Store Activities (repeat customers)."""

    list_display = [
        'user_email',
        'store_name',
        'scan_count',
        'total_points_earned',
        'total_spent_display',
        'first_scan',
        'last_scan'
    ]
    list_filter = ['store', 'first_scan', 'last_scan']
    search_fields = ['user__email', 'store__name']
    readonly_fields = [
        'user',
        'store',
        'scan_count',
        'total_points_earned',
        'total_spent',
        'first_scan',
        'last_scan',
        'last_updated'
    ]
    ordering = ['store', '-scan_count']
    actions = ['refresh_activities', 'export_to_csv']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'

    def store_name(self, obj):
        return obj.store.name
    store_name.short_description = 'Store'
    store_name.admin_order_field = 'store__name'

    def total_spent_display(self, obj):
        return f"{obj.total_spent:,.2f} RSD"
    total_spent_display.short_description = 'Total Spent'
    total_spent_display.admin_order_field = 'total_spent'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def refresh_activities(self, request, queryset):
        """Refresh user store activities."""
        AnalyticsService.update_user_store_activities()
        self.message_user(request, "User store activities refreshed.")
    refresh_activities.short_description = "Refresh all user-store activities"

    def export_to_csv(self, request, queryset):
        """Export activities to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_store_activities.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'User', 'Store', 'Scan Count', 'Points Earned',
            'Total Spent (RSD)', 'First Scan', 'Last Scan'
        ])

        for obj in queryset:
            writer.writerow([
                obj.user.email,
                obj.store.name,
                obj.scan_count,
                obj.total_points_earned,
                obj.total_spent,
                obj.first_scan.strftime('%Y-%m-%d %H:%M') if obj.first_scan else '',
                obj.last_scan.strftime('%Y-%m-%d %H:%M') if obj.last_scan else ''
            ])

        return response
    export_to_csv.short_description = "Export to CSV"


# Custom admin site configuration for Analytics section
class AnalyticsAdminSite(admin.AdminSite):
    site_header = "Loyalty App Analytics"
    site_title = "Analytics Dashboard"
    index_title = "Statistics & Reports"
