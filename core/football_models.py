from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _


class League(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return self.name


class Postition(models.Model):
    pass

class Footballer(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    age = models.IntegerField()
    nationality = CountryField(max_length=100)
    
    # def clean(self, *args, **kwargs):
    #     from django.core.exceptions import ValidationError
    #     reserved_numbers = self.get_all_reserved_numbers()
    #     print(reserved_numbers)
    #     if self.number in reserved_numbers:
    #         raise ValidationError(
    #             _(f"{self.number is reserved}"))
    #     super().clean(*args, **kwargs)

    # def get_all_reserved_numbers(self):
    #     reserved_numbers = []
    #     footballers =  Footballer.objects.filter(club__name=self.club.name)
    #     for footballer in footballers:
    #         reserved_numbers.append(footballer.number)
    #     return reserved_numbers
    
    def save(self, *args, **kwargs):
        self.clean(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Club(models.Model):
    division_name = models.ForeignKey(
        League, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    players = models.ForeignKey(Footballer, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Match(models.Model):

    class Meta:
        verbose_name_plural = "football matches"

    home_team = models.ForeignKey(Club,
                                  related_name='home_matches',
                                  on_delete=models.CASCADE)
    away_team = models.ForeignKey(Club,
                                  related_name='away_matches',
                                  on_delete=models.CASCADE)
    date = models.DateField()
    result = models.CharField(max_length=50)

    def clean(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if self.home_team == self.away_team:
            raise ValidationError(
                _("Same Team can not play against eatch other"))
        super().clean(*args, **kwargs)