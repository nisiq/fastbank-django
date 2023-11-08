"""
    Models de toda a aplicação
"""

from django.db import models 
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.utils import timezone


class UserManager(BaseUserManager):
    """ Manager for users """

    def create_user(self, email, password=None, **extra_fiels):
        """ Create, save and return a new user """
        if not email:
            raise ValueError("Usuario deve inserir o email")

        user = self.model(email=self.normalize_email(email), **extra_fiels)
        user.set_password(password)
    #Salvar Usuario
        user.save()

        return user

    def create_superuser(self, email, password):
        """ Create, save and return a new super user """
        user = self.create_user(email, password)
        user.is_staff = True 
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Mix de Permissões
class User(AbstractBaseUser, PermissionsMixin):
    """ User in system """
    # Email deve ser único
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=False)
    # Não pode ser null
    last_name = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=11, unique=True, null=False)
    # Url_imagem = models.ImageField(null=True), upload_to=user_image_field)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Quando foi criado
    created_at = models.DateTimeField(default=timezone.now)

    # Objetos disso serão gerenciados pelo UserManager
    objects = UserManager()

    # Para fazer login, campos utilizados
    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return f'self.{self.first_name} {self.last_name}'