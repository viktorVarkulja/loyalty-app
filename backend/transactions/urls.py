from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Receipt scanning
    path('receipts/scan/', views.scan_receipt, name='scan_receipt'),

    # Points balance
    path('points/balance/', views.get_points_balance, name='points_balance'),

    # Product review requests
    path('items/<str:item_id>/request-review/', views.request_item_review, name='request_item_review'),

    # Admin review endpoints
    path('reviews/pending/', views.get_pending_reviews, name='get_pending_reviews'),
    path('reviews/<str:item_id>/approve/', views.approve_review, name='approve_review'),
    path('reviews/<str:item_id>/reject/', views.reject_review, name='reject_review'),
]
