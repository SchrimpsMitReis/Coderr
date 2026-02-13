from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class OfferPagination(PageNumberPagination):
    """
    Pagination class for offer list endpoints.

    Properties:
    - Default page size: 10
    - Client may override page size via `?page_size=`
    - Maximum allowed page size: 100

    Response format:
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
        Builds the paginated response using the standard response structure.

        Notes:
        - `count` represents the total number of matching records
          (not only those on the current page).
        - `next` / `previous` contain navigation links or `None`.
        """
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
