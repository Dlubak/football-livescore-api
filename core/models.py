from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Manages user create/save
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with given
        email, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.clean_fields()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_field):
        """
        Creates and saves a superuser with the given email,
        nickname and password
        """
        user = self.create_user(email, password=password)
        user.is_staff = True
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
    name = models.CharField(_('name'), max_length=50, blank=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        """
        String representation of user model
        """
        return self.email
