from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reviews', views.ReviewRequestViewSet, basename='review')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Additional endpoints
    path('reviews/my/', views.my_review_requests, name='my_reviews'),
    path('reviews/pending/', views.pending_reviews, name='pending_reviews'),
]
