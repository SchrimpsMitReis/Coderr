from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders_app.api.views import OrderCountView, OrdersViewSet

"""
Routing configuration for Orders.

- /orders/ → CRUD operations handled via OrdersViewSet (router-based)
- /order-count/<user_id>/ → Returns the number of orders
  for a specific user, optionally filtered by status (?status=...)
"""
router = DefaultRouter()
router.register("orders", OrdersViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
    path("order-count/<int:pk>/", OrderCountView.as_view(), name="order-count-inprogress"),
    path("completed-order-count/<int:pk>/", OrderCountView.as_view(), name="order-count-complete"),
]