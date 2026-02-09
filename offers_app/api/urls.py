from django.urls import include, path
from rest_framework.routers import DefaultRouter
from offers_app.api.views import OfferViewSet, OfferdetailSingleView

router = DefaultRouter()
router.register("offers", OfferViewSet, basename="offers")

urlpatterns = [
    path('', include(router.urls), name="offer-list"),
    path('offerdetails/<int:pk>/', OfferdetailSingleView.as_view(), name='offerdetail-detail')
]
