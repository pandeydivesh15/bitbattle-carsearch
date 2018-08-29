from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^(?P<id>[A-Za-z0-9]+)/$', views.car_detail, name = "detail"),
]

