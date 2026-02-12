from django.urls import include, path

from general_app.api.views import BaseInfoView


"""
General API-Endpunkte.

Enthält systemweite Informationen,
die keiner spezifischen Business-App zugeordnet sind.
"""

urlpatterns = [
    path(
        'base-info/',
        BaseInfoView.as_view(),
        name='base-info'
    )
]