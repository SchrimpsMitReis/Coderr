from django.contrib import admin

from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "email", "created_at")
    list_filter = ("type",)
    search_fields = ("user__username", "email")