from django.urls import path, include
from rest_framework.routers import DefaultRouter
from football import views

router = DefaultRouter()
router.register(r'leagues', views.LeagueViewSet)
router.register(r'club', views.ClubViewSet)
router.register(r'pos', views.PositionViewSet)

app_name = 'football'
urlpatterns = [
    path(r'', include(router.urls)),
]
