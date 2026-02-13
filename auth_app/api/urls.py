from django.urls import include, path

from auth_app.api.views import RegistrationView, LoginView
"""
Authentication endpoints of the API.

- POST /registration/ → Registers a new user.
- POST /login/ → Authenticates user credentials.
"""
urlpatterns = [
    path(
        'registration/',
        RegistrationView.as_view(),
        name='user-registration'
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='user-login'
    ),
]