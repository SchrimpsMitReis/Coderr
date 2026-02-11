from django.urls import include, path

from auth_app.api.views import RegistrationView, LoginView

"""
Authentifizierungs-Endpunkte der API.

- POST /registration/ → Registriert einen neuen Benutzer.
- POST /login/ → Authentifiziert Benutzer-Credentials.
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