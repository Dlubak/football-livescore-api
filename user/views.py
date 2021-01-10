from django.contrib.auth import get_user_model
from rest_framework import generics
from user.serializers import UserSerializer
from rest_framework import permissions
from rest_framework import authentication
from user.permissions import IsOwner


class ListCreateUserView(generics.ListCreateAPIView):
    """
    Create a new user in the system
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    Manage the authenticated user
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [authentication.BasicAuthentication]
    queryset = get_user_model().objects.all()
