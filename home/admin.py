from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy  as _
from .models import *
# Register your models here.
from django.contrib.auth import get_user_model
class CustomUserAdmin(UserAdmin):
    '''Define admin model for custom User with no username field'''
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "auth_token",
                    "is_verified",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email",  "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name", "email")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    
admin.site.register(get_user_model(),CustomUserAdmin)
admin.site.register((BlogComment))
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=['title','description','thumbnail','author']