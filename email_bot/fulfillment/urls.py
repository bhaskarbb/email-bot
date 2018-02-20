from django.urls import path
from . import views

app_name = 'fulfillment'

urlpatterns = [
    path('', views.action_handler),

]
