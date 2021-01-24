# from rest_framework import mixins
from rest_framework import viewsets
from core import football_models
from football import serializers


class LeagueViewSet(viewsets.ModelViewSet):
    """
    Manage Leagues in the database
    """
    queryset = football_models.League.objects.all()
    serializer_class = serializers.LeagueSerializer


class ClubViewSet(viewsets.ModelViewSet):
    """
    Manage Clubs in the database
    """
    queryset = football_models.Club.objects.all()
    serializer_class = serializers.ClubSerializer


class PositionViewSet(viewsets.ModelViewSet):
    """
    Manage Positions in the database
    """
    queryset = football_models.Position.objects.all()
    serializer_class = serializers.PositionSerializer
