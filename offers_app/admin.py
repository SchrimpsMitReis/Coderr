from django.contrib import admin
from .models import Offer, OfferDetail

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "updated_at")
    search_fields = ("title", "user__username")
    list_filter = ("created_at", "updated_at")

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "offer", "offer_type", "price", "delivery_time_in_days")
    list_filter = ("offer_type",)