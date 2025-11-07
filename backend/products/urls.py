from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'stores', views.StoreViewSet, basename='store')

urlpatterns = [
    # Favorite stores (must be before router URLs to avoid conflicts)
    path('stores/favorites/', views.list_favorite_stores, name='list_favorite_stores'),
    path('stores/favorites/add/', views.add_favorite_store, name='add_favorite_store'),
    path('stores/favorites/<str:favorite_id>/', views.remove_favorite_store, name='remove_favorite_store'),

    # Router URLs
    path('', include(router.urls)),
]
