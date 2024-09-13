from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User


# Copied from my other project so change at will
class UserAdmin(BaseUserAdmin):
    # Things that are shown to all users
    list_display = (
        "username",
        "display_name",
        "birthday",
        "county",
        "interests",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "county")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("display_name", "birthday", "county", "interests")},
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "display_name",
                    "birthday",
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

# Unregister the group model from admin since we're not using it
admin.site.unregister(Group)
