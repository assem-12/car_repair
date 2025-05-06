from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser


User = get_user_model()

class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "user_id": user.id,
                    "is_admin": user.is_staff
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminOnlyView(views.APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return Response({"message": "You're an admin"})
