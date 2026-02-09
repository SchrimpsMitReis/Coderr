from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from auth_app.api.serializers import LoginSerializer, RegistrationSerializer
from auth_app.models import UserProfile
from rest_framework import status


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    data = {}

    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token = Token.objects.create(user=saved_account)
            data = {
                'token': token.key,
                'username' : saved_account.username,
                'email' : saved_account.email ,
                'user_id' : saved_account.id
            }

        else:
            data=serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data, status=status.HTTP_201_CREATED)
    
 
class LoginView(APIView):
    data = {}
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)            
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        data = {
                "token": token.key,
                "username" : user.username,
                "email" : user.email,
                "user_id" : user.id
            }
        return Response(data, status=status.HTTP_200_OK)
