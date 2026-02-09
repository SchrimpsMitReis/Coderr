from django.urls import include, path

from core.api.views import BaseInfoView


urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]
