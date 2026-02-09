from reviews_app.api.filter import ReviewFilter
from reviews_app.api.permissions import ReviewPermission
from reviews_app.api.serializers import ReviewListSerializer
from reviews_app.models import Review
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, ReviewPermission]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    # filterset_fields = ["business_user_id", "reviewer_id"]
    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]  # default ordering (Warnung weg, stabil)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)  # statt request.data mutieren



# class ReviewListView(ListCreateAPIView):
#     queryset= Review.objects.all()
#     serializer_class = ReviewListSerializer
#     pagination_class = None
#     permission_classes = [IsAuthenticated, ReviewPermission]
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ['business_user_id', 'reviewer_id']
#     ordering_fields = ['updated_at' , 'rating']
#     ordering = ['updated_at']



#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         user_id = request.user.id
#         data = request.data
#         data['reviewer'] = user_id
#         return self.create(request, *args, **kwargs)
    
# class ReviewSingleUpdateDeleteView(RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewListSerializer
#     permission_classes = [IsAuthenticated, ReviewPermission]

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

