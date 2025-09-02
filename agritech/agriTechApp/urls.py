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
    # 👇 Farmer Management (Admin only)
    path("farmers/", FarmerListCreateView.as_view(), name="farmers_list_create"),
    path("farmers/<int:pk>/", FarmerDetailView.as_view(), name="farmer_detail"),
    
    # 👇 Farmer Crop Management
    path("crops/", CropListCreateView.as_view(), name="crops"),  # farmers see own crops
    path("crops/<int:pk>/", CropDetailView.as_view(), name="crop_detail"),
    
     # 👇 Admin Crop Management
    path("admin-api/crops/", AdminCropListView.as_view(), name="admin_crops"),
    path("admin-api/crops/<int:pk>/", AdminCropDetailView.as_view(), name="admin_crop_detail"),
    
    # 🔹 New Admin Dashboard endpoint
    path("admin-api/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin-api/crops-per-farmer/", CropsPerFarmerView.as_view(), name="crops_per_farmer"),
    
    # 👇 Farmer Dashboard
    path("farmer/dashboard/", FarmerDashboardView.as_view(), name="farmer_dashboard"),
    path("farmer/crops-by-type/", FarmerCropsByTypeView.as_view(), name="farmer_crops_by_type"),
]