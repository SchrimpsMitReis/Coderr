from django.urls import include, path

from profile_app.api.views import BusinessListView, CustomerListView, ProfileDetailView


urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view() ,name='single-user-profile-info'),
    path('profiles/customer/', CustomerListView.as_view() ,name='customer-user-list'),
    path('profiles/business/', BusinessListView.as_view() ,name='business-user-list'),

]
