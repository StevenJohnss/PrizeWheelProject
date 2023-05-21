from django.contrib.auth.backends import BaseBackend

class TokenBackend(BaseBackend):
    def authenticate(self, request, token=None):
        # Implement your token authentication logic here
        pass


from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

class ExpiringTokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Token '):
            key = auth_header.split('Token ')[1]
            try:
                token = Token.objects.select_related('user').get(key=key)
            except Token.DoesNotExist:
                raise AuthenticationFailed('Invalid token')
            
            now = timezone.now()
            
            if token.created < now - timedelta(hours=8):
                raise AuthenticationFailed('Token has expired')

            # Assign the user to the request
            request.user = token.user

        return self.get_response(request)