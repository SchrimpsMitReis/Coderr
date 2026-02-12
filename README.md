# Coderr – Backend API with Django REST Framework

Coderr is a backend API for a freelancer and service marketplace platform.
The project is built with Django and Django REST Framework and models the typical workflows of such a platform: service providers create offers, customers place orders, and customers can leave reviews afterwards.

This repository contains the backend only. A frontend can be implemented separately and connected via the REST API.

## Overview

The API supports users with different roles, a clear separation of responsibilities, and a fine-grained permission system.
All interactions are handled via REST endpoints and secured using token-based authentication.

The main focus of the project is clean architecture, understandable permission logic, filtering capabilities, and comprehensive happy-path and unhappy-path testing.

## Features

Coderr includes the following core features:

– Token-based authentication
– Role system with Customer and Business users
– Offer management for business users
– Order creation and lifecycle handling
– Review system with one review per customer and business
– Action- and object-level permissions
– Filtering and ordering via query parameters
– Optional pagination
– Extensive automated test coverage

## Project Structure

The project is split into multiple Django apps, each covering a specific domain:

auth_app contains authentication and user profiles
offers_app manages offers and offer details
orders_app handles order creation and updates
reviews_app implements the review system
profile_app exposes profile-related endpoints
core contains shared utilities, base tests and helpers

## Installation

First, clone the repository and switch to the project directory:

`git clone https://github.com/SchrimpsMitReis/Coderr.git
cd Coderr`

Create and activate a virtual environment:

python -m venv env
source env/bin/activate       # macOS / Linux
env\Scripts\activate          # Windows


### Install dependencies:

`pip install -r requirements.txt`


### Run database migrations:

python manage.py makemigrations
python manage.py migrate


Optionally create a superuser for the Django admin interface:

python manage.py createsuperuser


Start the development server:

python manage.py runserver


The API will then be available at http://127.0.0.1:8000/.

Authentication

The API uses token-based authentication.
After logging in, a token is returned and must be sent with all authenticated requests:

Authorization: Token <your_token>

API Logic and Permissions

Access to the API is strictly controlled:

Customers are allowed to create orders and write reviews.
Business users can create and update offers and change the status of orders they are involved in.
Customers can only update or delete reviews they created themselves.
Both roles can only access objects they are involved in.
Delete operations are restricted to staff or admin users.

Permissions are implemented using custom permission classes and make use of both has_permission and has_object_permission.

Reviews – Special Rules

Each customer is allowed to create only one review per business user.
This rule is enforced on two levels:

– Serializer validation with a user-friendly error message
– A database-level unique constraint to prevent race conditions

The reviewer field is never accepted from client input and is always set automatically from the authenticated user.

Filtering, Ordering and Pagination

The API uses django-filter and DRF’s ordering backend.
Filters are applied exclusively via query parameters, for example:

GET /reviews/?business_user=3
GET /reviews/?ordering=-rating


Filtering logic is clearly separated from business logic.
Default ordering ensures consistent pagination results.

Testing

The project contains extensive automated tests covering:

– Happy-path scenarios
– Unhappy-path scenarios
– Permission enforcement
– Filtering and ordering behavior

Run all tests:

python manage.py test


Run only selected tests:

python manage.py test -k happy
python manage.py test -k unhappy


Or using tags:

python manage.py test --tag=happy
python manage.py test --tag=unhappy

Project Goal

Coderr is designed as a learning and portfolio project.
The main goals are:

– Clean REST architecture
– Realistic business rules
– Strong separation of concerns
– Testable and maintainable code
– Clear and transparent permission logic

The project can be used as a reference implementation for larger Django REST Framework backends or extended as a foundation for future ideas.

Author

Roman Schröder
Backend & API Development




Coderr – Backend API mit Django REST Framework

Coderr ist eine Backend-API für eine Freelancer- bzw. Marktplatz-Plattform.
Das Projekt wurde mit Django und Django REST Framework umgesetzt und bildet die typische Logik einer Plattform ab, auf der Anbieter Services einstellen können, Kunden Bestellungen auslösen und anschließend Bewertungen abgeben.

Das Repository enthält ausschließlich das Backend. Ein mögliches Frontend kann unabhängig davon angebunden werden.

Überblick

Die API unterstützt Benutzer mit unterschiedlichen Rollen, eine klare Trennung von Verantwortlichkeiten und ein fein abgestuftes Berechtigungssystem.
Alle Zugriffe erfolgen über REST-Endpoints, abgesichert durch Token-Authentifizierung.

Im Fokus des Projekts stehen saubere Architektur, verständliche Permissions, Filterlogik sowie umfangreiche Happy- und Unhappy-Tests.

Features

Coderr bietet unter anderem:

– Token-basierte Authentifizierung
– Rollenmodell mit Customer und Business-User
– Angebotsverwaltung für Business-User
– Bestellabwicklung für Kunden
– Bewertungssystem mit Einschränkung auf eine Bewertung pro Kunde und Anbieter
– Objekt- und Aktions-Permissions
– Filter, Ordering und optionale Pagination
– Umfangreiche automatisierte Tests

Projektstruktur

Das Projekt ist in mehrere Django-Apps aufgeteilt, die jeweils eine klar abgegrenzte Domäne abbilden:

auth_app enthält Authentifizierung und Benutzerprofile
offers_app verwaltet Angebote und Angebotsdetails
orders_app bildet den Bestellprozess ab
reviews_app enthält das Bewertungssystem
profile_app stellt Profilinformationen bereit
core enthält gemeinsame Utilities, Base-Tests und Hilfsklassen

Installation

Zunächst das Repository klonen und in das Projektverzeichnis wechseln:

git clone https://github.com/SchrimpsMitReis/Coderr.git
cd Coderr


Danach eine virtuelle Umgebung anlegen und aktivieren:

python -m venv env
source env/bin/activate       # macOS / Linux
env\Scripts\activate          # Windows


Abhängigkeiten installieren:

pip install -r requirements.txt


Migrationen ausführen und die Datenbank initialisieren:

python manage.py makemigrations
python manage.py migrate


Optional einen Superuser für das Admin-Interface erstellen:

python manage.py createsuperuser


Anschließend den Entwicklungsserver starten:

python manage.py runserver


Die API ist danach unter http://127.0.0.1:8000/ erreichbar.

Authentifizierung

Die API verwendet Token-Authentifizierung.
Nach dem Login wird ein Token ausgegeben, der bei weiteren Requests im Authorization-Header mitgesendet wird.

Authorization: Token <dein_token>

API-Logik und Permissions

Die Zugriffskontrolle ist strikt geregelt:

Customer dürfen Bestellungen erstellen und Bewertungen schreiben.
Business-User dürfen Angebote erstellen und bearbeiten sowie den Status von Bestellungen ändern, an denen sie beteiligt sind.
Customer dürfen nur ihre eigenen Reviews bearbeiten oder löschen.
Beide Rollen sehen ausschließlich Objekte, an denen sie beteiligt sind.
Löschoperationen sind auf Staff- oder Admin-Benutzer beschränkt.

Die Permissions sind in eigene Permission-Klassen ausgelagert und nutzen sowohl has_permission als auch has_object_permission.

Reviews – Besonderheiten

Ein Kunde darf einen Anbieter nur einmal bewerten.
Diese Regel wird doppelt abgesichert:

– durch Serializer-Validation (saubere Fehlermeldung)
– durch einen Datenbank-Constraint (UniqueConstraint), um Race-Conditions zu verhindern

Der reviewer wird niemals aus dem Request übernommen, sondern automatisch aus dem eingeloggten Benutzer gesetzt.

Filter, Ordering und Pagination

Die API nutzt django-filter und DRF-Ordering.
Filter werden ausschließlich über Query-Parameter gesteuert, zum Beispiel:

GET /reviews/?business_user=3
GET /reviews/?ordering=-rating


Filterspezifikation und Business-Logik sind klar getrennt.
Ordering erfolgt stabil über definierte Default-Felder, um inkonsistente Pagination zu vermeiden.

Tests

Das Projekt enthält umfangreiche automatisierte Tests für:

– Happy-Paths
– Unhappy-Paths
– Permissions
– Filter- und Ordering-Logik

Alle Tests ausführen:

python manage.py test


Gezielt nur bestimmte Tests ausführen:

python manage.py test -k happy
python manage.py test -k unhappy


Oder per Tagging:

python manage.py test --tag=happy
python manage.py test --tag=unhappy

Ziel des Projekts

Coderr ist als Lern- und Portfolio-Projekt konzipiert.
Der Fokus liegt auf:

– sauberer REST-Architektur
– realistischen Business-Regeln
– gut testbarem Code
– verständlicher Rollen- und Rechtevergabe

Das Projekt eignet sich als Grundlage für eigene Erweiterungen oder als Referenz für komplexere DRF-Backends.

Autor

Roman Schröder
Backend & API Development



