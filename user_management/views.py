from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from user_management import models
from user_management.filters import MatchingFilter, UsersFilter

from user_management.models import Interest, Message, Registration
from user_management.serializers import InterestSerializer, MessageSerializer, RegistrationSerializer


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Save user registration data in the database
            serializer.save()
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

@api_view(["GET"])
def country_list(request):
    countries = Registration.objects.values_list("country", flat=True).distinct()
    return Response({"countries": list(countries)})

class UsersByCountryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegistrationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UsersFilter  # Apply the custom filter here

    def get_queryset(self):
        country = self.request.query_params.get('country', None)
        
        
        # Get the logged-in user's gender
        user_gender = self.request.user.profile.gender 
        if not country:
            opposite_gender = 'female' if user_gender == 'male' else 'male'
            return Registration.objects.filter(gender=opposite_gender)  
        
        opposite_gender = 'female' if user_gender == 'male' else 'male'
        
        # Filter by country and the opposite gender
        return Registration.objects.filter(country__iexact=country, gender=opposite_gender)

class MatchingUsersView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Registration.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MatchingFilter

    def get_queryset(self):
        user = self.request.user

        try:
            user_profile = user.profile
        except Registration.DoesNotExist:
            return Registration.objects.none()

        # Get the user's country and address
        user_country = user_profile.country
        user_address = user_profile.address

        # Filter users by country (excluding the current user)
        queryset = Registration.objects.filter(country=user_country).exclude(user=user)

        # Optionally, filter users by partial address match
        if user_address:
            queryset = queryset.filter(address__icontains=user_address[:5])  # Matching partial address

        return queryset


class JustJoinedUsersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        user_gender = user.profile.gender
        opposite_gender = 'female' if user_gender == 'male' else 'male'

        # Filter by opposite gender and order by join_date in descending order
        return Registration.objects.filter(gender=opposite_gender).order_by('-id')


class PreferredEducationMatchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        # Get the user's Registration profile
        try:
            user_profile = user.profile  # Fetch the OneToOne related Registration object
        except Registration.DoesNotExist:
            return Registration.objects.none()  # Return empty queryset if profile is missing

        # Ensure user has gender and preferred education
        if not user_profile.gender or not user_profile.preferred_education:
            return Registration.objects.none()

        opposite_gender = 'female' if user_profile.gender.lower() == 'male' else 'male'

        # Filter opposite gender users whose education matches the user's preferred education
        matched_users = Registration.objects.filter(
            gender=opposite_gender,
            education=user_profile.preferred_education
        ).order_by('-id')  # Order by most recent first

        return matched_users
    
class PreferredLocationMatchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]  
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        # Get the user's Registration profile
        try:
            user_profile = user.profile  # Fetch the OneToOne related Registration object
        except Registration.DoesNotExist:
            return Registration.objects.none()  # Return empty queryset if profile is missing

        # Ensure user has gender and preferred education
        if not user_profile.gender or not user_profile.preferred_location:
            return Registration.objects.none()

        opposite_gender = 'female' if user_profile.gender.lower() == 'male' else 'male'

        matched_users = Registration.objects.filter(
            gender=opposite_gender,
            address=user_profile.preferred_location
        ).order_by('-id')  # Order by most recent first
        return matched_users

class MessageListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        receiver = request.user
        messages = Message.objects.filter(receiver=receiver).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    


class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Fetch logged-in user (sender)
        sender = request.user
        receiver_id = kwargs['receiver_id']

        # Ensure that receiver exists
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the message content from the request data
        message_content = request.data.get('message')

        if not message_content:
            return Response({'message': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the message in the database
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            message=message_content
        )

        return Response({'message': 'Message sent successfully'}, status=status.HTTP_201_CREATED)

class ConversationView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        username = self.kwargs.get('username')

        try:
            receiver = Registration.objects.get(user__username=username)
        except Registration.DoesNotExist:
            raise NotFound(detail="User not found")

        messages = Message.objects.filter(
            Q(sender=current_user, receiver=receiver.user) |
            Q(sender=receiver.user, receiver=current_user)
        ).order_by('timestamp')

        if not messages.exists():
            raise NotFound(detail="No conversation found with this user")

        return messages

class UserMessageListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user

        senders = Message.objects.filter(receiver=current_user).values_list('sender', flat=True).distinct()
        
        users = Registration.objects.filter(user__in=senders)
        return users

class UsersIMessagedView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        
        receivers = Message.objects.filter(sender=current_user).values_list('receiver', flat=True).distinct()

        users = Registration.objects.filter(user__in=receivers)
        return users

class SendInterestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        current_user = request.user
        
        # Check if the receiver exists
        try:
            receiver = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")

        # Check if the current user is not trying to express interest in themselves
        if current_user == receiver:
            return Response({"detail": "You cannot express interest in yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the interest
        interest = Interest.objects.create(sender=current_user, receiver=receiver)

        # Optionally, you can serialize the interest data and return it as a response
        serializer = InterestSerializer(interest)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InterestsReceivedView(generics.ListAPIView):
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return Interest.objects.filter(receiver=current_user).order_by('-created_at')

class InterestResponseView(generics.UpdateAPIView):
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        sender_username = self.kwargs.get('sender')
        receiver = self.request.user  # The current logged-in user is the receiver

        try:
            interest = Interest.objects.get(sender__username=sender_username, receiver=receiver)
        except Interest.DoesNotExist:
            raise NotFound(detail="Interest not found or you are not the receiver")

        return interest

    def patch(self, request, *args, **kwargs):
        interest = self.get_object()

        status_value = request.data.get('status')

        # Check if the status is valid
        if status_value not in dict(Interest.STATUS_CHOICES).keys():
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the interest status
        interest.status = status_value
        interest.save()

        # Return updated interest data as response
        return Response(self.serializer_class(interest).data, status=status.HTTP_200_OK)