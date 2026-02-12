from django.urls import include, path

from profile_app.api.views import BusinessListView, CustomerListView, ProfileDetailView

"""
URL-Routing für Profil-Endpunkte.

Endpunkte:
- /profile/<pk>/             -> Detailansicht eines einzelnen UserProfiles
- /profiles/customer/        -> Liste aller Customer-Profile
- /profiles/business/        -> Liste aller Business-Profile

Namenskonvention:
- single-user-profile-info   -> Detailansicht
- customer-user-list         -> Customer-Liste
- business-user-list         -> Business-Liste
"""

urlpatterns = [
    # Einzelnes Profil (Detailansicht)
    path(
        "profile/<int:pk>/",
        ProfileDetailView.as_view(),
        name="single-user-profile-info",
    ),

    # Alle Customer-Profile
    path(
        "profiles/customer/",
        CustomerListView.as_view(),
        name="customer-user-list",
    ),

    # Alle Business-Profile
    path(
        "profiles/business/",
        BusinessListView.as_view(),
        name="business-user-list",
    ),
]