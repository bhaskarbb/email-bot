from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'meeting'

urlpatterns = [
    path('', views.GetMeeting.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
