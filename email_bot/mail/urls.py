from django.urls import path
from . import views


app_name = 'mail'

urlpatterns = [
    path('', views.recieve_mail),
]
