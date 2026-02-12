from rest_framework.routers import DefaultRouter
from reviews_app.api.views import ReviewViewSet

"""
Routing für Review-Endpunkte.

Registriert das ReviewViewSet unter:
    /reviews/           -> List (GET), Create (POST)
    /reviews/<pk>/      -> Retrieve (GET), Update (PUT/PATCH), Delete (DELETE)

Router-Namenskonvention:
    reviews-list
    reviews-detail
"""

router = DefaultRouter()
router.register(
    r"reviews",
    ReviewViewSet,
    basename="reviews",  # notwendig, wenn queryset nicht direkt im ViewSet definiert ist
)

urlpatterns = router.urls