from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("profile/", UserProfileView.as_view(), name="profile"),  # farmers see own profile
    path("farmers/", FarmerListView.as_view(), name="farmers"),  # admin only
    path("crops/", CropListCreateView.as_view(), name="crops"),  # farmers see own crops
    path("crops/<int:pk>/", CropDetailView.as_view(), name="crop_detail"),
]