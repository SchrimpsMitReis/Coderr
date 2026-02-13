from django.urls import include, path

from profile_app.api.views import BusinessListView, CustomerListView, ProfileDetailView

"""
URL routing for profile-related endpoints.

Endpoints:
- /profile/<pk>/        → Detail view of a single UserProfile
- /profiles/customer/   → List of all customer profiles
- /profiles/business/   → List of all business profiles

Naming convention:
- single-user-profile-info → Detail view
- customer-user-list      → Customer list
- business-user-list      → Business list"""

urlpatterns = [
    path(
        "profile/<int:pk>/",
        ProfileDetailView.as_view(),
        name="single-user-profile-info",
    ),

    path(
        "profiles/customer/",
        CustomerListView.as_view(),
        name="customer-user-list",
    ),

    path(
        "profiles/business/",
        BusinessListView.as_view(),
        name="business-user-list",
    ),
]