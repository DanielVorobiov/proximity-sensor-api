import base64
import json
from datetime import datetime, timedelta, timezone

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import SensorRecord


class SensorRecordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        sensor_data = {
            "serial": "000100000100",
            "application": 11,
            "Time": "2022-11-08T04:00:04.317801",
            "Type": "xkgw",
            "device": "TestDevice",
            "v0": 100013,
            "v1": 0.69,
            "v2": 1.31,
            "v3": 0.18,
            "v4": 0,
            "v5": 0.8,
            "v6": 0,
            "v7": 26965,
            "v8": 0.1,
            "v9": 97757496,
            "v10": 0,
            "v11": 0,
            "v12": 1.84,
            "v13": 0,
            "v14": 0.7,
            "v15": 10010,
            "v16": 100013,
            "v17": 26965,
            "v18": 2.72,
        }
        self.valid_data = {
            "message": {
                "attributes": {"key": "value"},
                "data": base64.b64encode(
                    json.dumps(sensor_data).encode("utf-8")
                ).decode("utf-8"),
                "messageId": "2070443601311540",
                "message_id": "2070443601311540",
                "publishTime": "2021-02-26T19:13:55.749Z",
                "publish_time": "2021-02-26T19:13:55.749Z",
            },
            "subscription": "projects/myproject/subscriptions/mysubscription",
        }
        self.invalid_data = {"message": {"data": "invalid_base64"}}
        self.invalid_json = {
            "message": {
                "data": base64.b64encode(
                    "invalid_json".encode("utf-8")
                ).decode("utf-8"),
            }
        }

    def test_post_valid_data(self):
        response = self.client.post(
            "/api/sensor/", self.valid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorRecord.objects.count(), 1)

    def test_post_invalid_data(self):
        response = self.client.post(
            "/api/sensor/", self.invalid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SensorRecord.objects.count(), 0)
        self.assertIn("error", response.data)

    def test_post_invalid_json(self):
        response = self.client.post(
            "/api/sensor/", self.invalid_json, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SensorRecord.objects.count(), 0)
        self.assertIn("error", response.data)

    def test_get_sensor_data(self):
        SensorRecord.objects.create(
            sensor_id=1,
            human_presence=1,
            dwell_time=10,
            timestamp=(
                datetime.now(timezone.utc) - timedelta(hours=1)
            ).isoformat(),
        )
        SensorRecord.objects.create(
            sensor_id=2,
            human_presence=0,
            dwell_time=5,
            timestamp=(
                datetime.now(timezone.utc) - timedelta(days=2)
            ).isoformat(),
        )

        response = self.client.get("/api/sensor/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 2)

        response = self.client.get("/api/sensor/?sensor_id=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

        start_time = (datetime.now(timezone.utc) - timedelta(days=1)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        end_time = (datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
        response = self.client.get(
            f"/api/sensor/?start_time={start_time}&end_time={end_time}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_get_sensor_data_pagination(self):
        for i in range(50):
            SensorRecord.objects.create(
                sensor_id=i,
                human_presence=1,
                dwell_time=10,
                timestamp=datetime.now(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
            )

        response = self.client.get("/api/sensor/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 20)

        response = self.client.get("/api/sensor/?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 20)

        response = self.client.get("/api/sensor/?page=3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 10)

    def test_get_sensor_data_pagination_invalid(self):
        response = self.client.get("/api/sensor/?page=abc")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
