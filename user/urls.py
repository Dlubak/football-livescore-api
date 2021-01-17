"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from user import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
app_name = 'user'
urlpatterns = [
    path(r'users/', views.ListUserView.as_view(), name="list"),
    path(r'users/create', views.CreateUserView.as_view(), name="create"),
    path(r'users/<int:pk>', views.ManageUserView.as_view(), name="manage"),
    path(r'token/', views.CreateAuthToken.as_view(), name="token"),
]
