from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from auth_app.api.signals import User
from auth_app.models import UserProfile
from orders_app.api.permissions import OrdersPermission
from orders_app.api.serializers import OrderCountSerializer, OrderCreateSerializer, OrderSerializer, OrderUpdateSerializer
from orders_app.models import Orders
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404

class OrdersViewSet(ModelViewSet):
    """
    ViewSet for Orders (CRUD operations).

    Security and Business Rules:
    - Access restricted to authenticated users (IsAuthenticated).
    - Role-based and object-level rules enforced via OrdersPermission
      (Customer / Business / Admin).
    - Queryset is limited to orders in which the user is involved
      (either customer_user or business_user).

    Serializer strategy:
    - create → OrderCreateSerializer (input: offer_detail_id)
    - update / partial_update → OrderUpdateSerializer (status only)
    - default → OrderSerializer (read / response representation)
    """

    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, OrdersPermission]

    def get_queryset(self):
        """
        Returns only Orders in which the authenticated user is involved.

        This prevents users from accessing unrelated Orders,
        even if they attempt to guess or manually access object IDs.
        """
        user = self.request.user

        return super().get_queryset().filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def get_serializer_class(self):
        """
        Selects the appropriate serializer depending on the current action.
        """
        if self.action == "create":
            return OrderCreateSerializer

        if self.action in ("update", "partial_update"):
            return OrderUpdateSerializer

        return OrderSerializer


class OrderCountView(APIView):
    """
    Returns the number of Orders for a Business user, filtered by status.

    Current behavior:
    - The status is derived from the request path:
        - If the path contains 'complete' → COMPLETED
        - Otherwise → IN_PROGRESS
    - The response key depends on the status:
        - IN_PROGRESS → {"order_count": <int>}
        - COMPLETED  → {"completed_order_count": <int>}

    Note:
    - Path-based status switching works but is fragile.
      A cleaner approach would be using a query parameter
      (e.g., ?status=completed).
    """

    permission_classes = [IsAuthenticated]
    User = get_user_model()
    def get(self, request, pk):
        """
        Returns the order count for a specific Business user.

        pk: business_user_id (User ID of the business).
        """
        searched_status, prefix = self._resolve_status_from_path(request.path)
        user = get_object_or_404(User, pk=pk)
        count = Orders.objects.filter(
            business_user_id=pk,
            status=searched_status,
        ).count()

        return Response(
            {f"{prefix}order_count": count},
            status=status.HTTP_200_OK,
        )

    def _resolve_status_from_path(self, path):
        """
        Determines the order status and response key prefix
        based on the request path.

        Returns:
        - Tuple: (Orders.StatusType, response_prefix)
        """
        if "complete" in path:
            return Orders.StatusType.COMPLETED, "completed_"

        return Orders.StatusType.IN_PROGRESS, ""
