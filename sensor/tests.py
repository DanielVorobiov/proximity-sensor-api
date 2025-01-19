import base64
import json

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

    def test_post_valid_data(self):
        response = self.client.post(
            "/api/sensor_data/", self.valid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorRecord.objects.count(), 1)
