"""Sensor data views."""

import base64
import json

from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SensorRecord
from .serializers import SensorRecordSerializer


class SensorRecordView(APIView):
    """API view for handling sensor data.

    This view provides endpoints for creating and retrieving sensor
    data.
    """

    def post(self, request):
        """Create new sensor data records.

        Decodes base64-encoded sensor data from the request,
        validates it, and saves it to the database.
        Args:
            request (rest_framework.request.Request): The HTTP request object.
        Returns:
            rest_framework.response.Response:
            A response indicating success or failure.
        """
        try:
            data = request.data
            decoded_data = base64.b64decode(data["message"]["data"]).decode(
                "utf-8"
            )
            sensor_data = json.loads(decoded_data)

            serializer = SensorRecordSerializer(
                data={
                    "sensor_id": sensor_data["v0"],
                    "human_presence": sensor_data["v11"],
                    "dwell_time": sensor_data["v18"],
                    "timestamp": sensor_data["Time"],
                }
            )

            if serializer.is_valid():
                # validated_data.append(serializer.validated_data)
                serializer.save()
                return Response(
                    {"message": "Data saved successfully!"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # SensorRecord.objects.bulk_create(
            #     [SensorRecord(**data) for data in validated_data]
            # )

        except json.JSONDecodeError as e:
            return Response(
                {"error": f"Invalid JSON data: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """Retrieve sensor data.

        Query parameters:
            - sensor_id (optional): Filter by sensor ID;
            - start_time (optional): Filter by start timestamp
                                        (ISO 8601 format);
            - end_time (optional): Filter by end timestamp (ISO 8601 format);
            - page (optional): Page number for pagination;
            - page_size (optional): Number of items per page.
        Args:
            request (rest_framework.request.Request): The HTTP request object.
        Returns:
            rest_framework.response.Response:
            A response containing paginated sensor data.
        """
        try:
            sensor_id = request.GET.get("sensor_id")
            start_time = request.GET.get("start_time")
            end_time = request.GET.get("end_time")
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 20))

            queryset = SensorRecord.objects.all()

            if sensor_id:
                queryset = queryset.filter(sensor_id=sensor_id)
            if start_time and end_time:
                queryset = queryset.filter(
                    timestamp__range=[start_time, end_time]
                )

            paginator = Paginator(queryset, page_size)
            try:
                page_obj = paginator.page(page)
            except Exception:
                raise Http404("Invalid page number")

            serializer = SensorRecordSerializer(page_obj, many=True)
            return Response(
                {
                    "data": serializer.data,
                }
            )

        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Http404 as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
