import json
import unittest

from api import create_app, db
from api.water_quality.models import Record


class WaterQualityTestCase(unittest.TestCase):
    def setUp(self):
        # Create the Flask app with a testing config.
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

        # Create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables
        with self.app.app_context():
            db.drop_all()

    def test_get_empty_records(self):
        """Test GET /water-quality/records returns an empty list when no records exist."""
        response = self.client.get("/water-quality/records")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_add_record(self):
        """Test POST /water-quality/records creates a new record."""
        record_data = {
            "location": "Test Location",
            "ph_level": 7.0,
            "turbidity": 5.0,
            "temperature": 20.0,
        }
        response = self.client.post(
            "/water-quality/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        # Check that the returned record matches the input
        self.assertEqual(data["location"], record_data["location"])
        self.assertEqual(data["ph_level"], record_data["ph_level"])
        self.assertEqual(data["turbidity"], record_data["turbidity"])
        self.assertEqual(data["temperature"], record_data["temperature"])
        self.assertIn("recorded_at", data)

    def test_get_record(self):
        """Test GET /water-quality/records/<id> returns the correct record."""
        # Create a record first
        record_data = {
            "location": "Test Location",
            "ph_level": 7.2,
            "turbidity": 4.5,
            "temperature": 18.0,
        }
        post_response = self.client.post(
            "/water-quality/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        # Retrieve the created record's ID from the database
        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        # Now get the record by id
        get_response = self.client.get(f"/water-quality/records/{record_id}")
        self.assertEqual(get_response.status_code, 200)
        data = json.loads(get_response.data)
        self.assertEqual(data["location"], record_data["location"])
        self.assertEqual(data["ph_level"], record_data["ph_level"])
        self.assertEqual(data["turbidity"], record_data["turbidity"])
        self.assertEqual(data["temperature"], record_data["temperature"])

    def test_get_record_not_found(self):
        """Test GET /water-quality/records/<id> for a non-existent record returns 404."""
        response = self.client.get("/water-quality/records/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_record(self):
        """Test DELETE /water-quality/records/<id> deletes the record."""
        # First create a record
        record_data = {
            "location": "Delete Test",
            "ph_level": 7.0,
            "turbidity": 3.0,
            "temperature": 22.0,
        }
        post_response = self.client.post(
            "/water-quality/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        # Delete the record
        delete_response = self.client.delete(f"/water-quality/records/{record_id}")
        self.assertEqual(delete_response.status_code, 200)
        data = json.loads(delete_response.data)
        self.assertEqual(data["message"], "Record soft-deleted successfully")

        # Verify the record is gone
        get_response = self.client.get(f"/water-quality/records/{record_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_record_not_found(self):
        """Test DELETE /water-quality/records/<id> for a non-existent record returns 404."""
        response = self.client.delete("/water-quality/records/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
