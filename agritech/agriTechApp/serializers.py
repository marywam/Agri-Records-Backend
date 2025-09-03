from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import *

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name",  "phone_number", "location", "farm_size","date_of_birth", "gender", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data.get("phone_number"),
            location=validated_data.get("location"),
            farm_size=validated_data.get("farm_size"),
            date_of_birth=validated_data.get("date_of_birth"),
            gender=validated_data.get("gender"),
            password=validated_data["password"],
            role="farmer"
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ["id", "name", "type", "quantity", "planted_date", "harvested", "farmer"]
        read_only_fields = ["farmer"]  # Farmers cannot assign crops to others



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "role", "phone_number", "location",  "farm_size",  "date_of_birth", "gender"]
        read_only_fields = ["email", "role"]
        
class AdminDashboardSerializer(serializers.Serializer):
    total_farmers = serializers.IntegerField()
    total_crops = serializers.IntegerField()
    
class CropsPerFarmerSerializer(serializers.Serializer):
    username = serializers.CharField()
    total_crops = serializers.IntegerField()

class FarmerDashboardSerializer(serializers.Serializer):
    total_crops = serializers.IntegerField()
  
class CropsByTypeSerializer(serializers.Serializer):
    type = serializers.CharField()
    total = serializers.IntegerField()

    

