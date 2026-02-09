from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from auth_app.models import UserProfile
from profile_app.api.serializers import ProfileSerializer




class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "pk"

class CustomerListView(ListAPIView):
    pagination_class = None
    queryset = UserProfile.objects.filter(type = "customer")
    serializer_class = ProfileSerializer

class BusinessListView(ListAPIView):
    pagination_class = None
    queryset = UserProfile.objects.filter(type = "business")
    serializer_class = ProfileSerializer
