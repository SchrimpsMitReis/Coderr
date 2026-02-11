from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders_app.api.views import OrderCountView, OrdersViewSet

router = DefaultRouter()
router.register("orders", OrdersViewSet, basename="orders")

urlpatterns = [
    path('', include(router.urls) , name='orders-list'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count-inprogress' ),
    path('completed-order-count/<int:pk>/', OrderCountView.as_view(), name='order-count-complete' )

]
