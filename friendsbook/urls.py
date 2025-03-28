from django.contrib import admin
from django.urls import path, include
from user_management.views import ConversationView, InterestResponseView, InterestsReceivedView, JustJoinedUsersView, LoginView, LogoutView, MessageListView,PreferredEducationMatchView, PreferredLocationMatchView, SendInterestView, SendMessageView, UserMessageListView,  UserProfileUpdateView, UserRegistrationView, UserProfileView, UsersByCountryView, UsersIMessagedView, country_list, MatchingUsersView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<str:username>/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get token
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("countries/", country_list, name="country_list"),
    path("countries/users/", UsersByCountryView.as_view(), name="users_by_country"),
    path('matching-users/', MatchingUsersView.as_view(), name='matching-users'),
    path('just_joined/', JustJoinedUsersView.as_view(), name='just_joined_users'),
    path('preferred/education/', PreferredEducationMatchView.as_view(), name='preferred-education'),
    path('preferred/location/', PreferredLocationMatchView.as_view(), name='preferred-location'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('send-message/<int:receiver_id>', SendMessageView.as_view(), name='send-message'),
    path('conversation/<str:username>/', ConversationView.as_view(), name='conversation'),
    path('users/messaged-me/', UserMessageListView.as_view(), name='users-messaged-me'),
    path('users/i-messaged/', UsersIMessagedView.as_view(), name='users-i-messaged'),
    path('interest/send/<str:username>/', SendInterestView.as_view(), name='send_interest'),
    path('interests/received/', InterestsReceivedView.as_view(), name='interests_received'),
    path('interest/respond/<str:sender>/', InterestResponseView.as_view(), name='interest_respond'),
  
    # path('auth/', include('rest_framework.urls'))
]
