from django.urls import path

from . import views

app_name = 'soundscape'
urlpatterns = [
    path('', views.homepage, name='homepage'),
]
