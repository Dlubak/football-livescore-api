from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.permissions import IsOwnerOrAdmin
from user.serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ListUserView(generics.ListAPIView):
    """
    List all users in the system
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    Manage the authenticated user
    """
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin, permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = get_user_model().objects.all()
    
    # def get_object(self):
    #     """
    #     Retrieve and return authentication user
    #     """
    #     return self.request.user


class CreateAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
