from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fulfillment.urls')),
    path('meeting', include('meeting.urls')),
    path('mail', include('mail.urls')),
    path('user', include('user.urls'))
]
