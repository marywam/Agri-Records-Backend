from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import *
from .permissions import IsAdmin, IsFarmer, IsOwnerOrAdmin
from django.db.models import Count
from .models import *

User = get_user_model()


# Farmer Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# Farmer Login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(email=serializer.validated_data["email"], password=serializer.validated_data["password"])

        if not user:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role,
            }
        })
        

# Profile View (farmer can only see/update self)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        return self.request.user



# Farmer Management (Admin only)
class FarmerListView(generics.ListAPIView):
    queryset = User.objects.filter(role="farmer")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


# Crop Management
# Crop Management
class CropListCreateView(generics.ListCreateAPIView):
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmer | IsAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Crop.objects.all()
        return Crop.objects.filter(farmer=user)  # 👈 Farmers see only their crops

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)  # 👈 Force ownership



class CropDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        data = {
            "total_farmers": User.objects.filter(role="farmer").count(),
            "total_crops": Crop.objects.count(),
        }
        serializer = AdminDashboardSerializer(data)
        return Response(serializer.data)

class CropsPerFarmerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        data = (
            Crop.objects.values("farmer__username")
            .annotate(total_crops=Count("id"))
            .order_by("farmer__username")
        )

        # Map to serializer structure
        results = [
            {"username": item["farmer__username"], "total_crops": item["total_crops"]}
            for item in data
        ]

        serializer = CropsPerFarmerSerializer(results, many=True)
        return Response(serializer.data)
    
# Admin Farmer Management
class FarmerListCreateView(generics.ListCreateAPIView):
    """Admin can list all farmers and create a new one"""
    queryset = User.objects.filter(role="farmer")
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        # force role to farmer (admins cannot create other admins this way)
        serializer.save(role="farmer")


class FarmerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin can view, edit or delete a farmer"""
    queryset = User.objects.filter(role="farmer")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
# Admin Crop Management
class AdminCropListView(generics.ListAPIView):
    """Admin can view all crops"""
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class AdminCropDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin can edit or delete any crop"""
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
class FarmerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request):
        total_crops = Crop.objects.filter(farmer=request.user).count()
        data = {"total_crops": total_crops}
        serializer = FarmerDashboardSerializer(data)
        return Response(serializer.data)
    
class FarmerCropsByTypeView(APIView):
    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request):
        data = (
            Crop.objects.filter(farmer=request.user)
            .values("type")
            .annotate(total=Count("id"))
            .order_by("type")
        )

        serializer = CropsByTypeSerializer(data, many=True)
        return Response(serializer.data)

