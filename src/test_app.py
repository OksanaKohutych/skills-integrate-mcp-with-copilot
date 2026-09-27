import json
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


class ActivityPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.app_path = Path(__file__).resolve().with_name("app.py")
        self.activities_path = self.app_path.with_name("activities.json")
        if self.activities_path.exists():
            self.activities_path.unlink()

    def test_signup_persists_to_json_file(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("activity_app", self.app_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        client = TestClient(module.app)
        email = "persist@mergington.edu"

        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.activities_path.exists())

        saved = json.loads(self.activities_path.read_text())
        self.assertIn(email, saved["Chess Club"]["participants"])


if __name__ == "__main__":
    unittest.main()
