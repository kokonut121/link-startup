from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

class UserAdmin(BaseUserAdmin):
    # Fields that are shown to all users
    list_display = (
        "username",
        "display_name",
        "year_in_highschool",
        "county",
        "interests",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "county")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("display_name", "year_in_highschool", "county", "interests")},
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "display_name",
                    "year_in_highschool",
                    "county",
                    "interests",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("username", "display_name")
    ordering = ("username",)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)