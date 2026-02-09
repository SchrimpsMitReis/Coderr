from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
import random
import string

from offers_app.models import Offer, OfferDetail
from orders_app.models import Orders
from reviews_app.models import Review



class UnauthenificatedAPITestCase(APITestCase):
    def setUp(self):
        self.user_business = self.create_user_object("KimPossible", UserProfile.UserType.BUSINESS)
        self.user_customer = self.create_user_object("JamesBond")
        self.create_offer_objects()
        self.create_offer_detail_objects()
        self.order_1 = self.create_order_objects()
        self.order_2 = self.create_order_objects()
        self.review_1 = self.create_review_objects()
        super().setUp()

    def create_user_data(self):
        return {
            'username': "exampleUsername",
            'email': "example@mail.de",
            'password': 'examplePassword',
            'repeated_password' : 'examplePassword',
            'type' : "customer"
        }
    
    def create_user_object(self, name= "testUser", type = UserProfile.UserType.CUSTOMER):
        
        user = User.objects.create_user(
            username=name,
            email="test@example.com",
            password="Password123!",
        )
        profile = UserProfile.objects.create(
            user=user,
            email=user.email,
            type=type,  
        )
        return user
    
    def create_offer_objects(self):
        self.offer_1 = Offer.objects.create(
            user = self.user_business,
            title = "Grafik",
            image = "",
            description = "Wer reitet so spät durch Nacht und Wind?",
        )
        self.offer_2 = Offer.objects.create(
            user = self.user_business,
            title = "Grafik",
            image = "",
            description = "Wer reitet so spät durch Nacht und Wind?",
        )

    def create_offer_detail_objects(self):
        self.offer_detail_basic_1 = OfferDetail.objects.create(
            offer = self.offer_1,
            title = "MedienUndSo",
            revisions = 3,
            delivery_time_in_days = 5,
            price = 100,
            features = ["Logo Design", "Käsekuchen"],
            offer_type = "basic"
        )
        self.offer_detail_standard_1 = OfferDetail.objects.create(
            offer = self.offer_1,
            title = "MedienUndSo",
            revisions = 3,
            delivery_time_in_days = 5,
            price = 200,
            features = ["Logo Design", "Käsekuchen"],
            offer_type = "standard"
        )
        self.offer_detail_premium_1 = OfferDetail.objects.create(
            offer = self.offer_1,
            title = "MedienUndSo",
            revisions = 3,
            delivery_time_in_days = 5,
            price = 400,
            features = ["Logo Design", "Käsekuchen"],
            offer_type = "premium"
        )
        self.offer_detail_basic_2 = OfferDetail.objects.create(
            offer = self.offer_2,
            title = "MedienUndSo",
            revisions = 3,
            delivery_time_in_days = 5,
            price = 100,
            features = ["Logo Design", "Käsekuchen"],
            offer_type = "basic"
        )
        self.offer_detail_standard_2 = OfferDetail.objects.create(
            offer = self.offer_2,
            title = "MedienUndSo",
            revisions = 3,
            delivery_time_in_days = 5,
            price = 200,
            features = ["Logo Design", "Käsekuchen"],
            offer_type = "standard"
        )
        self.offer_detail_premium_2 = OfferDetail.objects.create(
            offer = self.offer_2,
            title = "MedienUndSo",
            revisions = 3,
            delivery_time_in_days = 5,
            price = 400,
            features = ["Logo Design", "Käsekuchen"],
            offer_type = "premium"
        )

    def create_order_objects(self):
        detail = self.offer_detail_basic_1
        return Orders.objects.create(
            customer_user = self.user_customer,
            business_user = self.user_business,
            title = detail.title,
            revisions = detail.revisions,
            delivery_time_in_days = detail.delivery_time_in_days,
            price = detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status=Orders.StatusType.IN_PROGRESS,
        )

    def create_review_objects(self):
        return Review.objects.create(
            business_user = self.user_business,
            reviewer = self.user_customer,
            rating = 5,
            description = "Hatta doll jemaat"
        )


class AuthenificatedAPITestCaseCustomer(UnauthenificatedAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.user = self.user_customer
        token, _ = Token.objects.get_or_create(user=self.user)

        # 👇 DAS ist die Authentifizierung
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

class AuthenificatedAPITestCaseBusiness(UnauthenificatedAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.user = self.user_business
        token, _ = Token.objects.get_or_create(user=self.user)

        # 👇 DAS ist die Authentifizierung
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )
