
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
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, OrdersPermission]    
    
    def get_queryset(self):
        user = self.request.user
        return Orders.objects.filter(Q(customer_user=user) | Q(business_user=user))
    
    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        if self.action in ["update", "partial_update"]:
            return OrderUpdateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)    

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    


class OrderCountView(APIView):
    
    def get(self, request, pk):
        
        path = request.path
        searched_status = Orders.StatusType.COMPLETED
        prefix = 'completed_'
        if 'complete' not in path:
            searched_status =  Orders.StatusType.IN_PROGRESS
            prefix = ''

        count = Orders.objects.filter(
            business_user_id = pk,
            status = searched_status
            ).count()
        
        return Response({f'{prefix}order_count' : count}, status=status.HTTP_200_OK)