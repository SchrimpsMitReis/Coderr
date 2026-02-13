from django.urls import include, path
from rest_framework.routers import DefaultRouter
from offers_app.api.views import OfferViewSet, OfferdetailSingleView

"""
Routing configuration for offer-related endpoints.

- /offers/ → Full CRUD functionality provided by the OfferViewSet (via router)
- /offerdetails/<pk>/ → Retrieve a single OfferDetail instance
"""
router = DefaultRouter()
router.register("offers", OfferViewSet, basename="offers")

urlpatterns = [
    path("", include(router.urls)),
    path("offerdetails/<int:pk>/", OfferdetailSingleView.as_view(), name="offerdetail-detail"),
]