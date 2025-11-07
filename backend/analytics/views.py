"""
API views for Analytics endpoints.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import (
    StoreAnalytics,
    ProductAnalytics,
    UserActivityLog,
    StoreProductRanking,
    UserStoreActivity
)
from .serializers import (
    StoreAnalyticsSerializer,
    ProductAnalyticsSerializer,
    UserActivityLogSerializer,
    StoreProductRankingSerializer,
    UserStoreActivitySerializer
)
from .services import AnalyticsService


class StoreAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Store Analytics.
    Read-only access with caching for performance.
    """
    queryset = StoreAnalytics.objects.select_related('store').all()
    serializer_class = StoreAnalyticsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Refresh all store analytics."""
        AnalyticsService.update_store_analytics()
        return Response({'status': 'success', 'message': 'Store analytics refreshed'})

    @action(detail=True, methods=['post'])
    def refresh_single(self, request, pk=None):
        """Refresh analytics for a single store."""
        analytics = self.get_object()
        AnalyticsService.update_store_analytics(store_id=analytics.store.id)
        return Response({'status': 'success', 'message': f'Analytics refreshed for {analytics.store.name}'})


class ProductAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Product Analytics.
    Read-only access with caching for performance.
    """
    queryset = ProductAnalytics.objects.select_related('product').all()
    serializer_class = ProductAnalyticsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Refresh all product analytics."""
        AnalyticsService.update_product_analytics()
        return Response({'status': 'success', 'message': 'Product analytics refreshed'})


class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User Activity Logs.
    Read-only access.
    """
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class StoreProductRankingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Store Product Rankings.
    """
    queryset = StoreProductRanking.objects.select_related('store', 'product').all()
    serializer_class = StoreProductRankingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """Filter by store if provided."""
        queryset = super().get_queryset()
        store_id = self.request.query_params.get('store_id')

        if store_id:
            queryset = queryset.filter(store_id=store_id)

        return queryset


class UserStoreActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User Store Activities (repeat customers).
    """
    queryset = UserStoreActivity.objects.select_related('user', 'store').all()
    serializer_class = UserStoreActivitySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """Filter by store if provided."""
        queryset = super().get_queryset()
        store_id = self.request.query_params.get('store_id')

        if store_id:
            queryset = queryset.filter(store_id=store_id)

        return queryset


# ==================== CUSTOM API ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def store_rankings(request):
    """
    Get store rankings by scans or points.
    Query params:
    - by: 'scans' or 'points' (default: scans)
    - limit: number of results (default: 10)
    """
    by = request.query_params.get('by', 'scans')
    limit = int(request.query_params.get('limit', 10))

    if by == 'points':
        data = AnalyticsService.get_store_rankings_by_points(limit=limit)
    else:
        data = AnalyticsService.get_store_rankings_by_scans(limit=limit)

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def weekly_activity_trend(request):
    """
    Get weekly activity trend.
    Query params:
    - weeks: number of weeks to include (default: 12)
    """
    weeks = int(request.query_params.get('weeks', 12))
    data = AnalyticsService.get_weekly_activity_trend(weeks=weeks)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def monthly_activity_trend(request):
    """
    Get monthly activity trend.
    Query params:
    - months: number of months to include (default: 12)
    """
    months = int(request.query_params.get('months', 12))
    data = AnalyticsService.get_monthly_activity_trend(months=months)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def daily_activity_trend(request):
    """
    Get daily activity trend.
    Query params:
    - days: number of days to include (default: 30)
    """
    days = int(request.query_params.get('days', 30))
    data = AnalyticsService.get_daily_activity_trend(days=days)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def most_scanned_products(request):
    """
    Get most scanned products by store.
    Query params:
    - store_id: filter by specific store (optional)
    - limit: number of results (default: 10)
    """
    store_id = request.query_params.get('store_id')
    limit = int(request.query_params.get('limit', 10))

    data = AnalyticsService.get_most_scanned_products_by_store(
        store_id=store_id,
        limit=limit
    )
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def store_detailed_report(request):
    """
    Get comprehensive report for a specific store.
    Query params:
    - store_id: required
    - days: number of days to include (default: 30)
    """
    store_id = request.query_params.get('store_id')
    if not store_id:
        return Response(
            {'error': 'store_id parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    days = int(request.query_params.get('days', 30))
    data = AnalyticsService.get_store_detailed_report(store_id=store_id, days=days)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def top_repeat_customers(request):
    """
    Get top repeat customers for a store.
    Query params:
    - store_id: required
    - limit: number of results (default: 10)
    """
    store_id = request.query_params.get('store_id')
    if not store_id:
        return Response(
            {'error': 'store_id parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    limit = int(request.query_params.get('limit', 10))
    data = AnalyticsService.get_top_repeat_customers(store_id=store_id, limit=limit)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def new_product_scan_frequency(request):
    """
    Get frequency of new products being scanned.
    Query params:
    - days: number of days to include (default: 30)
    """
    days = int(request.query_params.get('days', 30))
    data = AnalyticsService.get_new_product_scan_frequency(days=days)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def new_products_growth(request):
    """
    Track growth of new unique products being scanned.
    Query params:
    - days: number of days to include (default: 30)
    """
    days = int(request.query_params.get('days', 30))
    data = AnalyticsService.get_new_products_growth(days=days)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_leaderboard(request):
    """
    Get user leaderboard by points.
    Query params:
    - limit: number of results (default: 20)
    """
    limit = int(request.query_params.get('limit', 20))
    data = AnalyticsService.get_user_leaderboard(limit=limit)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def store_leaderboard(request):
    """
    Get comprehensive store leaderboard.
    Query params:
    - limit: number of results (default: 20)
    """
    limit = int(request.query_params.get('limit', 20))
    data = AnalyticsService.get_store_leaderboard(limit=limit)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def product_leaderboard(request):
    """
    Get product leaderboard by scan count.
    Query params:
    - limit: number of results (default: 20)
    """
    limit = int(request.query_params.get('limit', 20))
    data = AnalyticsService.get_product_leaderboard(limit=limit)
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def refresh_all_analytics(request):
    """
    Trigger a full refresh of all cached analytics data.
    This can be resource-intensive and should be used sparingly.
    """
    try:
        AnalyticsService.update_all_analytics()
        return Response({
            'status': 'success',
            'message': 'All analytics data has been refreshed'
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
