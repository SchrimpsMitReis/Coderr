from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile

from offers_app.models import Offer, OfferDetail
from orders_app.models import Orders
from reviews_app.models import Review



class UnauthenticatedAPITestCase(APITestCase):
    """
    Basis-TestCase, der eine konsistente Testdaten-Welt aufbaut.

    Erstellt:
    - 1 Business-User + Profil
    - 1 Customer-User + Profil
    - 2 Offers + OfferDetails (basic/standard/premium)
    - 2 Orders (auf Basis eines OfferDetails)
    - 1 Review

    Vorteil:
    - Tests können ohne viel Boilerplate direkt auf vorhandene Objekte zugreifen.

    Nachteil:
    - Für sehr einfache Tests (z.B. login) werden mehr Daten erstellt als nötig.
    """

    DEFAULT_LOGIN_PASSWORD = "Password123!"
    REGISTRATION_PASSWORD = "examplePassword"

    def setUp(self):
        super().setUp()

        self.user_business = self._create_user("KimPossible", UserProfile.UserType.BUSINESS)
        self.user_customer = self._create_user("JamesBond", UserProfile.UserType.CUSTOMER)

        self._create_offers()
        self._create_offer_details()

        self.order_1 = self._create_order()
        self.order_2 = self._create_order()

        self.review_1 = self._create_review()

    def create_user_data(self):
        """Payload für Registration-Tests."""
        return {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": self.REGISTRATION_PASSWORD,
            "repeated_password": self.REGISTRATION_PASSWORD,
            "type": "customer",
        }

    def _create_user(self, username = "exampleUsername", user_type = UserProfile.UserType.CUSTOMER):
        """
        Erstellt einen Django User + UserProfile.
        E-Mail wird aus dem Username abgeleitet, um Kollisionen zu vermeiden.
        """
        user = User.objects.create_user(
            username=username,
            email=f"{username.lower()}@example.com",
            password=self.DEFAULT_LOGIN_PASSWORD,
        )
        UserProfile.objects.create(user=user, email=user.email, type=user_type)
        return user

    def _create_offers(self):
        """Erstellt zwei Offers für den Business-User."""
        self.offer_1 = Offer.objects.create(
            user=self.user_business,
            title="Grafik",
            image="",
            description="Wer reitet so spät durch Nacht und Wind?",
        )
        self.offer_2 = Offer.objects.create(
            user=self.user_business,
            title="Grafik",
            image="",
            description="Wer reitet so spät durch Nacht und Wind?",
        )

    def _create_offer_details(self):
        """Erstellt OfferDetails (basic/standard/premium) für beide Offers."""
        self.offer_detail_basic_1 = self._create_offer_detail(self.offer_1, 100, "basic")
        self.offer_detail_standard_1 = self._create_offer_detail(self.offer_1, 200, "standard")
        self.offer_detail_premium_1 = self._create_offer_detail(self.offer_1, 400, "premium")

        self.offer_detail_basic_2 = self._create_offer_detail(self.offer_2, 100, "basic")
        self.offer_detail_standard_2 = self._create_offer_detail(self.offer_2, 200, "standard")
        self.offer_detail_premium_2 = self._create_offer_detail(self.offer_2, 400, "premium")

    def _create_offer_detail(self, offer, price, offer_type):
        """Erstellt ein OfferDetail mit Standardwerten."""
        return OfferDetail.objects.create(
            offer=offer,
            title="MedienUndSo",
            revisions=3,
            delivery_time_in_days=5,
            price=price,
            features=["Logo Design", "Käsekuchen"],
            offer_type=offer_type,
        )

    def _create_order(self):
        """Erstellt eine Order aus dem basic Detail von offer_1."""
        detail = self.offer_detail_basic_1
        return Orders.objects.create(
            customer_user=self.user_customer,
            business_user=self.user_business,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status=Orders.StatusType.IN_PROGRESS,
        )

    def _create_review(self):
        """Erstellt eine Review vom Customer für den Business."""
        return Review.objects.create(
            business_user=self.user_business,
            reviewer=self.user_customer,
            rating=5,
            description="Hatta doll jemaat",
        )


class AuthenticatedAPITestCaseCustomer(UnauthenticatedAPITestCase):
    """BaseCase für Requests als authentifizierter Customer."""

    def setUp(self):
        super().setUp()
        self.user = self.user_customer
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


class AuthenticatedAPITestCaseBusiness(UnauthenticatedAPITestCase):
    """BaseCase für Requests als authentifizierter Business-User."""

    def setUp(self):
        super().setUp()
        self.user = self.user_business
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")