from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        email = kwargs.get('Email')
        password = kwargs.get('password')

        try:
            user = User.objects.get(email=email);
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            
        except User.DoesNotExist:
            return None