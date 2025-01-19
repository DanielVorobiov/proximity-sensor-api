"""Endpoints for the sensord data app"""

from django.urls import path

from .views import SensorRecordView

urlpatterns = [
    path("sensor/", SensorRecordView.as_view(), name="sensor"),
]
