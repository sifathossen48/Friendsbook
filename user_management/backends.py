from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            if '@' in username:
                try:
                    user = User.objects.get(profile__email=username)
                except ObjectDoesNotExist:
                    return None
            elif username.isdigit():
                user = User.objects.get(profile__phone_number=username)
            else:
                user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None