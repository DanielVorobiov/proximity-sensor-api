from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Proximity Sensor API",
        default_version="v0.1",
        description="API to ingest and offer proximity sensor data.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
