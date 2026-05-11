from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the admin list view
    list_display = ('first_name','last_name', 'corporate_id', 'role', 'is_staff')
    
    # Add fields to the "Edit User" page
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'corporate_id')}),
    )
    
    # Add fields to the "Create User" page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'corporate_id')}),
    )