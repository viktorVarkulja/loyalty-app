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
]
