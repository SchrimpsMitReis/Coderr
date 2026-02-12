📦 Coderr – Backend API with Django REST Framework

A backend API for a freelancer and service marketplace platform.
Built with Django and Django REST Framework.

Coderr models the core workflows of a typical service platform:

Business users create offers

Customers place orders

Customers leave reviews

Permissions enforce clear role separation

This repository contains the backend only.

🚀 Overview

Coderr provides:

A clear role system (Customer / Business)

Token-based authentication

Object-level and action-level permission logic

Filtering and ordering via query parameters

Optional pagination

Comprehensive automated test coverage

The project focuses on:

Clean REST architecture

Realistic business rules

Separation of concerns

Maintainable and testable code

🧩 Features

🔐 Token-based authentication

👥 Role system (Customer & Business users)

📝 Offer management

📦 Order lifecycle handling

⭐ Review system (1 review per customer & business)

🛡️ Custom permissions (has_permission & has_object_permission)

🔎 Filtering & ordering

📄 Optional pagination

🧪 Extensive happy-path & unhappy-path testing

🏗 Project Structure

The project is split into domain-specific Django apps:

auth_app       → authentication & user profiles
offers_app     → offers and offer details
orders_app     → order workflow & status handling
reviews_app    → review system
profile_app    → profile endpoints
core           → shared utilities, base tests & helpers

⚙️ Installation
1️⃣ Clone repository
git clone https://github.com/SchrimpsMitReis/Coderr.git
cd Coderr

2️⃣ Create virtual environment
python -m venv env


Activate:

# macOS / Linux
source env/bin/activate

# Windows
env\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ (Optional) Create superuser
python manage.py createsuperuser

6️⃣ Start development server
python manage.py runserver


API runs at:

http://127.0.0.1:8000/

🔑 Authentication

The API uses Token Authentication.

After login, include the token in every authenticated request:

Authorization: Token <your_token>

🔐 API Logic & Permissions

Access rules are strictly enforced:

Customers

Can create orders

Can write reviews

Can update/delete their own reviews

Business Users

Can create & update offers

Can change status of their involved orders

Both Roles

Can only access objects they are involved in

Delete Operations

Restricted to staff or admin users

Permissions are implemented via custom classes using:

has_permission

has_object_permission

⭐ Reviews – Special Rules

Each customer can review a business user only once.

Enforced on two levels:

Serializer validation (user-friendly error)

Database-level UniqueConstraint (race condition protection)

The reviewer field is always set from request.user.

🔎 Filtering, Ordering & Pagination

Coderr uses:

django-filter

DRF OrderingFilter

Example queries:

GET /reviews/?business_user_id=3
GET /reviews/?ordering=-rating


Filtering is separated from business logic.

Default ordering ensures stable results.

🧪 Testing

Comprehensive automated test coverage includes:

Happy-path scenarios

Unhappy-path scenarios

Permission enforcement

Filtering & ordering behavior

Run all tests:

python manage.py test


Run specific tests:

python manage.py test --tag=happy
python manage.py test --tag=unhappy

🎯 Project Goal

Coderr is designed as a portfolio & learning project with focus on:

Clean architecture

Strong separation of concerns

Real-world permission logic

Structured, testable backend systems

It can serve as a foundation for larger DRF projects.

👨‍💻 Author

Roman Schröder
Backend & API Development

🇩🇪 Coderr – Backend API mit Django REST Framework

(Deutsche Version für Portfolio oder Recruiter)

Coderr ist eine Backend-API für eine Freelancer-Marktplatzplattform, entwickelt mit Django und Django REST Framework.

Die Anwendung bildet typische Marktplatzprozesse ab:

Anbieter erstellen Angebote

Kunden platzieren Bestellungen

Kunden hinterlassen Bewertungen

Das Repository enthält ausschließlich das Backend.

🧠 Fokus des Projekts

Saubere REST-Architektur

Durchdachte Rollen- & Permission-Logik

Objekt- und Aktions-Permissions

Strukturierter, testbarer Code

Klare Trennung von Business-Logik und Filterlogik

🔐 Sicherheitskonzept

Token-Authentifizierung

Objektbezogene Zugriffsprüfung

Rollenbasierte Rechte

Doppelte Absicherung kritischer Regeln (Serializer + DB Constraint)

🧪 Tests

Das Projekt enthält umfangreiche automatisierte Tests für:

Happy-Paths

Unhappy-Paths

Permissions

Filterlogik

💡 Einsatzmöglichkeiten

Coderr kann verwendet werden als:

Referenzprojekt für DRF-Architektur

Lernprojekt für komplexe Permission-Systeme

Grundlage für weitere Erweiterungen