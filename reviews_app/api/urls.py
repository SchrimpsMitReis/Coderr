from rest_framework.routers import DefaultRouter
from reviews_app.api.views import ReviewViewSet

"""
Routing configuration for review endpoints.

Registers the ReviewViewSet under:
    /reviews/      → List (GET), Create (POST)
    /reviews/<pk>/ → Retrieve (GET), Update (PUT/PATCH), Delete (DELETE)

Router naming convention:
    reviews-list
    reviews-detail"""

router = DefaultRouter()
router.register(
    r"reviews",
    ReviewViewSet,
    basename="reviews",  # notwendig, wenn queryset nicht direkt im ViewSet definiert ist
)

urlpatterns = router.urls