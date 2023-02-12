from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import GroupAdminForm

User = get_user_model()
# Unregister the original Group admin.
admin.site.unregister(Group)


# Create a new Group admin.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ["permissions"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
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
