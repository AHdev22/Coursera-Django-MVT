from django.contrib import admin
from django.urls import path

from littlelemon import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]
