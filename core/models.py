from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Manages user create/save
    """

    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with given 
        email, nickname, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email,
        nickname and password
        """
        user = self.create_user(email, name=name, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses e-mail instead of username
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    name = models.CharField(_('name'), max_length=50, blank=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


def __str__(self):
    """
    String representation of user model
    """
    return self.email
