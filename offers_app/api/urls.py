from django.urls import include, path
from rest_framework.routers import DefaultRouter
from offers_app.api.views import OfferViewSet, OfferdetailSingleView

"""
Routing für Offer- und OfferDetail-Endpunkte.

- /offers/ ... CRUD via ViewSet (Router)
- /offerdetails/<pk>/ ... Detailansicht eines OfferDetails
"""

router = DefaultRouter()
router.register("offers", OfferViewSet, basename="offers")

urlpatterns = [
    path("", include(router.urls)),
    path("offerdetails/<int:pk>/", OfferdetailSingleView.as_view(), name="offerdetail-detail"),
]