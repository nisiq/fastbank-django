"""
View for the user API
Configurar Requisições
"""

from rest_framework.response import Response
from rest_framework import (
    status,
    generics 
)

from rest_framework_simplejwt import authentication as authenticationJWT
from user.serializers import UserSerializer
from user.permissions import IsCreationOrIsAuthenticated


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the systems """
    serializer_class = UserSerializer


class ManagerUserAPiView(generics.RetrieveUpdateAPIView):
    """ Manage for the authenicated """