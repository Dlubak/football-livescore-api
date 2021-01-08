from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
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


class League(models.Model):
    name = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return self.name


class Club(models.Model):
    division_name = models.ForeignKey(
        League, related_name="division_name", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Footballer(models.Model):
    POSTION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('CB', 'Centre Back'),
        ('LB', 'Left Back'),
        ('RB', 'Right Back'),
        ('CM', 'Centre Midfielder'),
        ('LW', 'Left Winger'),
        ('RW', 'Right Winger'),
        ('ST', 'Striker'),
    ]
    name = models.CharField(max_length=100)
    club = models.ForeignKey('Club', on_delete=models.DO_NOTHING)
    number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    age = models.IntegerField()
    position = models.CharField(max_length=2,
                                choices=POSTION_CHOICES)
    nationality = CountryField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.position}"


class Match(models.Model):

    class Meta:
        verbose_name_plural = "football matches"

    home_team = models.ForeignKey(Club,
                                  related_name='home_matches',
                                  on_delete=models.CASCADE)
    away_team = models.ForeignKey(Club,
                                  related_name='away_matches',
                                  on_delete=models.CASCADE)
    home_team_players = models.ManyToManyField(
        'Footballer', related_name='home_team_players')
    away_team_players = models.ManyToManyField(
        'Footballer', related_name='away_team_players')
    date = models.DateField()

    def clean(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if self.home_team == self.away_team:
            raise ValidationError(
                _("Same Team can not play against eatch other"))
        super().clean(*args, **kwargs)
