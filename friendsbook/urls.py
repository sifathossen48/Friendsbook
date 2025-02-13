
from django.contrib import admin
from django.urls import path, include

from user_management.views import LoginView, LogoutView, UserProfileUpdateView, UserRegistrationView, UserProfileView
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
    # path('auth/', include('rest_framework.urls'))
]
