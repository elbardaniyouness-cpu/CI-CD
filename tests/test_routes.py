"""
Counter Service API tests

Run with:
    nosetests -v --with-coverage --cover-package=service
"""
from unittest import TestCase
from service import app
from service.common import status
from service.routes import reset_counters


class CounterTest(TestCase):
    """Tests for the Counter Service routes"""

    def setUp(self):
        self.client = app.test_client()
        reset_counters()

    def test_health(self):
        """It should be healthy"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["status"], "OK")

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["name"], "Counter Service")

    def test_create_counter(self):
        """It should create a counter"""
        resp = self.client.post("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        self.assertEqual(data["name"], "foo")
        self.assertEqual(data["counter"], 0)

    def test_duplicate_counter(self):
        """It should return 409 for a duplicate counter"""
        self.client.post("/counters/foo")
        resp = self.client.post("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def test_list_counters(self):
        """It should list all counters"""
        self.assertEqual(self.client.get("/counters").get_json(), [])
        self.client.post("/counters/foo")
        self.client.post("/counters/bar")
        resp = self.client.get("/counters")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.get_json()), 2)

    def test_read_counter(self):
        """It should read a counter"""
        self.client.post("/counters/foo")
        resp = self.client.get("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["counter"], 0)

    def test_read_missing_counter(self):
        """It should return 404 when reading a missing counter"""
        resp = self.client.get("/counters/missing")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_counter(self):
        """It should increment a counter"""
        self.client.post("/counters/foo")
        resp = self.client.put("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["counter"], 1)
        resp = self.client.put("/counters/foo")
        self.assertEqual(resp.get_json()["counter"], 2)

    def test_update_missing_counter(self):
        """It should return 404 when incrementing a missing counter"""
        resp = self.client.put("/counters/missing")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_counter(self):
        """It should delete a counter"""
        self.client.post("/counters/foo")
        resp = self.client.delete("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get("/counters/foo")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.patch("/counters")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
