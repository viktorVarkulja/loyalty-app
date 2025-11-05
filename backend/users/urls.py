from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from . import webshop_views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile
    path('profile/', views.get_user_profile, name='user_profile'),
    path('profile/update/', views.update_user_profile, name='update_profile'),
]

# Webshop API endpoints (separate from auth)
webshop_urlpatterns = [
    path('points/get/', webshop_views.webshop_get_points, name='webshop_get_points'),
    path('points/use/', webshop_views.webshop_use_points, name='webshop_use_points'),
    path('points/add/', webshop_views.webshop_add_points, name='webshop_add_points'),
]
