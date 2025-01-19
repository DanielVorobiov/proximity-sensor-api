"""Database models."""

from django.db import models


class SensorRecord(models.Model):
    sensor_id = models.IntegerField(db_index=True)
    human_presence = models.BooleanField()
    dwell_time = models.FloatField()
    timestamp = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ["-timestamp"]
