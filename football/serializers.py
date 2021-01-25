from rest_framework import serializers
from core import football_models
from django_countries.serializer_fields import CountryField


class LeagueSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)
    """
    Serializer for League Objects
    """
    class Meta:
        model = football_models.League
        fields = ('id', 'name', 'country',)
        read_only_fields = ('id',)


class ClubSerializer(serializers.ModelSerializer):
    league = serializers.StringRelatedField()
    """
    Serializer for Club Objects
    """
    class Meta:
        model = football_models.Club
        fields = ('id', 'name', 'league')
        read_only_fields = ('id',)


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer for Position Objects
    """
    class Meta:
        model = football_models.Position
        fields = ('id', 'short_name', 'long_name')
        read_only_fields = ('id',)
