from django.urls import include, path

from general_app.api.views import BaseInfoView


urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]
