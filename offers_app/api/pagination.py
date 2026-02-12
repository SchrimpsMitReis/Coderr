from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class OfferPagination(PageNumberPagination):
    """
    Pagination-Klasse für Offer-Listenendpunkte.

    Eigenschaften:
    - Standard-Seitengröße: 10
    - Client darf Seitengröße über `?page_size=` überschreiben
    - Maximal erlaubte Seitengröße: 100

    Response-Format:
    {
        "count": <int>,
        "next": <url|null>,
        "previous": <url|null>,
        "results": [...]
    }
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Baut die paginierte Antwort im gewünschten Standardformat.

        Hinweis:
        - `count` ist die Gesamtanzahl aller Treffer (nicht nur der aktuellen Seite).
        - `next`/`previous` sind Navigationslinks oder `None`.
        """
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )