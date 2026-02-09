from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):          #this is a custom admin for more hide ta password mostly
    list_display=['email','first_name','last_name','is_active']
    fieldsets=()


admin.site.register(User,UserAdmin)