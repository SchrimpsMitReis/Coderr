from django.contrib import admin
from .models import Orders

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_user", "business_user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_user__username", "business_user__username", "title")