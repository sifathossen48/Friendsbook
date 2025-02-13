from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from user_management.models import Registration
from user_management.serializers import RegistrationSerializer


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer  
    
    def create(self, request, *args, **kwargs):
        response_data = {
            "message": "User registration successful!",
            
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = RegistrationSerializer  # Use the same serializer for profile view
 
    def get_object(self):
        username = self.kwargs['username']
        try:
            registration = Registration.objects.get(user__username=username)
            return registration
        except Registration.DoesNotExist:
            raise NotFound(detail="User profile not found")

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile 
        except Registration.DoesNotExist:
            raise NotFound("User profile not found")

    def patch(self, request, *args, **kwargs):  
        profile = self.get_object()
        print("Received Data:", request.data)  # Debugging log
        
        serializer = self.get_serializer(profile, data=request.data, partial=True)  # Allow partial updates
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        print("Errors:", serializer.errors)  # Debugging log
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username_or_email_or_phone = request.data.get("username")  
        password = request.data.get("password")
        
        user = authenticate(request, username=username_or_email_or_phone, password=password)

        if user:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'access_token': access_token,
                'refresh_token': str(refresh)
            })
        return Response({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the refresh token
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"message": "Successfully logged out!"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)