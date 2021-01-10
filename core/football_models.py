from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _


class League(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return self.name


class Club(models.Model):
    league = models.ForeignKey(
        League, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Position(models.Model):
    short_name = models.CharField(max_length=3)
    long_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.long_name} - {self.short_name}"


class Player(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    age = models.IntegerField()
    nationality = CountryField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)

    def clean(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        reserved_numbers = self._get_all_reserved_numbers()
        print(reserved_numbers)
        if self.number in reserved_numbers:
            raise ValidationError(
                _(f"{self.number} is reserved"))
        super().clean(*args, **kwargs)

    def _get_all_reserved_numbers(self):
        reserved_numbers = []
        players = Player.objects.filter(club__name=self.club.name)
        for player in players:
            reserved_numbers.append(player.number)
        return reserved_numbers

    def save(self, *args, **kwargs):
        self.clean(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Contract(models.Model):
    pass


class Match(models.Model):
    home_team = models.ForeignKey(Club,
                                  related_name='home_matches',
                                  on_delete=models.CASCADE)
    away_team = models.ForeignKey(Club,
                                  related_name='away_matches',
                                  on_delete=models.CASCADE)
    date = models.DateField()
    home_team_score = models.IntegerField()
    away_team_score = models.IntegerField()

    class Meta:
        verbose_name = "Football Exhibition"

    def clean(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if self.home_team == self.away_team:
            raise ValidationError(
                _("Same Team can not play against eatch other"))
        super().clean(*args, **kwargs)

    def __str__(self):
        return f"{self.home_team} - {self.away_team}"
