
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from auth_app.models import UserProfile
from orders_app.api.permissions import OrdersPermission
from orders_app.api.serializers import OrderCountSerializer, OrderCreateSerializer, OrderSerializer, OrderUpdateSerializer
from orders_app.models import Orders
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics


class OrdersViewSet(ModelViewSet):
    """
    ViewSet für Orders (CRUD).

    Sicherheits-/Business-Regeln:
    - Zugriff nur für authentifizierte User (IsAuthenticated)
    - Rollen- und Objektregeln über OrdersPermission (Customer/Business/Admin)
    - Queryset ist auf Orders eingeschränkt, an denen der User beteiligt ist
      (customer_user oder business_user).

    Serializer-Strategie:
    - create: OrderCreateSerializer (Input: offer_detail_id)
    - update/partial_update: OrderUpdateSerializer (nur status)
    - sonst: OrderSerializer (Read / Response)
    """

    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, OrdersPermission]

    def get_queryset(self):
        """
        Liefert nur Orders, an denen der eingeloggte User beteiligt ist.

        Dadurch können User weder fremde Orders sehen noch über IDs erraten/abrufen,
        selbst wenn sie die Permission passieren würden.
        """
        user = self.request.user
        return super().get_queryset().filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def get_serializer_class(self):
        """
        Wählt je nach Action den passenden Serializer.
        """
        if self.action == "create":
            return OrderCreateSerializer
        if self.action in ("update", "partial_update"):
            return OrderUpdateSerializer
        return OrderSerializer


class OrderCountView(APIView):
    """
    Zählt Orders eines Business-Users nach Status.

    Aktuelles Verhalten:
    - Der Status wird anhand des URL-Pfads bestimmt:
        - enthält der Pfad 'complete' -> COMPLETED
        - sonst -> IN_PROGRESS
    - Response-Key ist abhängig vom Status:
        - IN_PROGRESS -> {"order_count": <int>}
        - COMPLETED  -> {"completed_order_count": <int>}

    Hinweis:
    - Das URL-basierte Status-Switching funktioniert, ist aber fragil.
      Cleanere Alternative wäre ein QueryParam (z.B. ?status=completed).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Gibt den Count für Orders eines Business-Users zurück.

        pk: business_user_id (User-ID des Business)
        """
        searched_status, prefix = self._resolve_status_from_path(request.path)

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
        Leitet Status und Response-Prefix aus dem Request-Pfad ab.

        Rückgabe:
        - (Orders.StatusType, prefix_string)
        """
        if "complete" in path:
            return Orders.StatusType.COMPLETED, "completed_"
        return Orders.StatusType.IN_PROGRESS, ""

