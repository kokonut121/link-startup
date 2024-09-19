from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Opportunity


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "display_name",
                    "year_in_highschool",
                    "county",
                    "interests",
                    "title",
                    "university",
                    "num_connections",
                    "avatar",
                    "connected",
                    "activity",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
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
    list_display = ("username", "display_name", "is_staff", "is_superuser")
    search_fields = ("username", "display_name")
    ordering = ("username",)


admin.site.register(User, UserAdmin)
admin.site.register(Opportunity)
