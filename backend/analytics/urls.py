"""
URL configuration for Analytics API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'store-analytics', views.StoreAnalyticsViewSet, basename='store-analytics')
router.register(r'product-analytics', views.ProductAnalyticsViewSet, basename='product-analytics')
router.register(r'activity-logs', views.UserActivityLogViewSet, basename='activity-logs')
router.register(r'store-product-rankings', views.StoreProductRankingViewSet, basename='store-product-rankings')
router.register(r'user-store-activities', views.UserStoreActivityViewSet, basename='user-store-activities')

urlpatterns = [
    # Custom endpoints for advanced queries
    path('store-rankings/', views.store_rankings, name='store-rankings'),
    path('weekly-trend/', views.weekly_activity_trend, name='weekly-trend'),
    path('monthly-trend/', views.monthly_activity_trend, name='monthly-trend'),
    path('daily-trend/', views.daily_activity_trend, name='daily-trend'),
    path('most-scanned-products/', views.most_scanned_products, name='most-scanned-products'),
    path('store-report/', views.store_detailed_report, name='store-report'),
    path('top-repeat-customers/', views.top_repeat_customers, name='top-repeat-customers'),
    path('new-product-frequency/', views.new_product_scan_frequency, name='new-product-frequency'),
    path('new-products-growth/', views.new_products_growth, name='new-products-growth'),
    path('user-leaderboard/', views.user_leaderboard, name='user-leaderboard'),
    path('store-leaderboard/', views.store_leaderboard, name='store-leaderboard'),
    path('product-leaderboard/', views.product_leaderboard, name='product-leaderboard'),
    path('refresh-all/', views.refresh_all_analytics, name='refresh-all'),

    # Router URLs
    path('', include(router.urls)),
]
