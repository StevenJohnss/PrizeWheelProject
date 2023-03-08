"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    SpinSerializer,
    UserPrizeSerializer,
    ResetUserPasswordSerializer
)
from core.models import Spin, UserPrize, ResetUserPassword


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserSpinsView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = SpinSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Spin.objects.all()
    
    #if removed: AssertionError: Expected view UserSpinsView to be called with a URL keyword argument named "pk". Fix your URL conf, or set the `.lookup_field` attribute on the view correctly.
    def get_object(self):
        """Filter queryset to authenticated user."""
        return self.queryset.get(
            user=self.request.user,
            user__is_active=True
        )


class UserPrizesView(generics.CreateAPIView, generics.ListAPIView):
    """Manage the authenticated user."""
    serializer_class =UserPrizeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserPrize.objects.all()
    
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(
            user=self.request.user,
            user__is_active=True
        )
        
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


class ResetUserPasswordView(generics.CreateAPIView ,generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = ResetUserPasswordSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ResetUserPassword.objects.all()
    
    def get_object(self):
        """Filter queryset to authenticated user."""
        return self.queryset.get(
            user=self.request.user,
            user__is_active=True,
            temp_pass= self.kwargs['uuid'],  
        )
    
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)