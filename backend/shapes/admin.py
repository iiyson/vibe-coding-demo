from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShapeItem, User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_admin",)
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_admin",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("is_admin",)}),
    )


@admin.register(ShapeItem)
class ShapeItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "color", "shape_type", "timestamp"]

