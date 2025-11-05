from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile
    path('profile/', views.get_user_profile, name='user_profile'),
    path('profile/update/', views.update_user_profile, name='update_profile'),
]
