from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', "phone_number", "location", "farm_size", 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name','phone_number')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    # Fields shown in the detail/edit view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','phone_number', 'location','farm_size','date_of_birth', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Info', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when creating a new user in Admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',"phone_number", "location", "farm_size", 'role', 'password1', 'password2'),
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        # For existing users, don't allow changing role if they're superuser
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.is_superuser:
            form.base_fields['role'].disabled = True
        return form

class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'farmer', 'planted_date', 'harvested')
    list_filter = ('type', 'harvested', 'planted_date')
    search_fields = ('name', 'farmer__email', 'farmer__username')
    list_editable = ('harvested',)
    date_hierarchy = 'planted_date'
    
    # For farmers, only show their own crops
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        return qs.filter(farmer=request.user)
    
    # For farmers, only allow editing their own crops
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser or request.user.role == 'admin':
            return True
        return obj.farmer == request.user
    
    # For farmers, only allow deleting their own crops
    def has_delete_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser or request.user.role == 'admin':
            return True
        return obj.farmer == request.user
    
    # When adding a new crop, set the farmer to the current user if they're a farmer
    def save_model(self, request, obj, form, change):
        if not change and request.user.role == 'farmer':
            obj.farmer = request.user
        super().save_model(request, obj, form, change)

# Register your models with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Crop, CropAdmin)