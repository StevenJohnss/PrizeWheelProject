"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
import datetime

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    SpinSerializer,
    UserPrizeSerializer,
    ResetUserPasswordSerializer,
    ResetUserPasswordCreateSerializer,
)
from core.models import Spin, UserPrize, ResetUserPassword, User


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    #email:stev@example.com
    #pass:123
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


@extend_schema_view(
    post=extend_schema(
        parameters=[
            OpenApiParameter(name='email', description='ex: steven@example.com', type=OpenApiTypes.STR ),
            OpenApiParameter(name='url', description='rest password apge url', type=OpenApiTypes.STR ),
        ]
    )
)
class ResetUserPasswordView(generics.CreateAPIView):
    """Manage the authenticated user."""
    serializer_class = ResetUserPasswordCreateSerializer
    
    def perform_create(self, serializer):
        """Create a new temp pass for the user."""
        email= self.request.query_params.get('email',None)
        selected_user= User.objects.get(email=email)
        if selected_user is not None:
            serializer.save(user=selected_user)
        else:
            raise Exception("User email Not found")
        
        
class ResetUserPasswordDeatilView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = ResetUserPasswordSerializer
    queryset = ResetUserPassword.objects.all()
    
    def get_object(self):
        """Filter queryset to authenticated user."""
        res = self.queryset.get(
            user__is_active=True,
            temp_pass__iexact= self.kwargs['uuid'],  
        )
        
        if res.expiers_at <= datetime.now():
            res.is_active=False 
            res.save()
            return Response("link expired", status.HTTP_400_BAD_REQUEST)
        
        return res
    
