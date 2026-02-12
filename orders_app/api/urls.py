from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders_app.api.views import OrderCountView, OrdersViewSet

"""
Routing für Orders.

- /orders/ ... CRUD via OrdersViewSet (Router)
- /order-count/<user_id>/ ... Anzahl Orders für User, optional gefiltert nach Status (?status=...)
"""

router = DefaultRouter()
router.register("orders", OrdersViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
    path("order-count/<int:pk>/", OrderCountView.as_view(), name="order-count-inprogress"),
    path("completed-order-count/<int:pk>/", OrderCountView.as_view(), name="order-count-complete"),
]