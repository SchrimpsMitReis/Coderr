from django.urls import include, path

from general_app.api.views import BaseInfoView


"""
General API endpoints.

Provides system-level information
that is not bound to a specific application domain.
"""
urlpatterns = [
    path(
        'base-info/',
        BaseInfoView.as_view(),
        name='base-info'
    )
]
