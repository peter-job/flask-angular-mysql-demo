import json
import unittest

from api import create_app, db
from api.blueprints.records.models import Record


class BaseTestCase(unittest.TestCase):
    """Base test case that sets up the Flask application and database."""

    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()


class TestRecordsGET(BaseTestCase):
    """Tests for GET /records and GET /records/<id> routes."""

    def test_get_empty_records(self):
        """GET /records returns an empty list when no records exist."""
        response = self.client.get("/records")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [])

    def test_get_record(self):
        """GET /records/<id> returns the correct record."""
        record_data = {
            "location": "Test Location",
            "ph_level": 7.2,
            "turbidity": 4.5,
            "temperature": 18.0,
        }
        post_response = self.client.post(
            "/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        get_response = self.client.get(f"/records/{record_id}")
        self.assertEqual(get_response.status_code, 200)
        data = get_response.get_json()
        self.assertEqual(data["location"], record_data["location"])
        self.assertEqual(data["ph_level"], record_data["ph_level"])
        self.assertEqual(data["turbidity"], record_data["turbidity"])
        self.assertEqual(data["temperature"], record_data["temperature"])

    def test_get_record_not_found(self):
        """GET /records/<id> for a non-existent record returns 404."""
        response = self.client.get("/records/999")
        self.assertEqual(response.status_code, 404)

    def test_get_record_invalid_id(self):
        """GET /records/<id> with a non-integer id returns 404."""
        response = self.client.get("/records/not-an-integer")
        self.assertEqual(response.status_code, 404)


class TestRecordsPOST(BaseTestCase):
    """Tests for POST /records route."""

    def test_add_record(self):
        """POST /records creates a new record."""
        record_data = {
            "location": "Test Location",
            "ph_level": 7.0,
            "turbidity": 5.0,
            "temperature": 20.0,
        }
        response = self.client.post(
            "/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["location"], record_data["location"])
        self.assertEqual(data["ph_level"], record_data["ph_level"])
        self.assertEqual(data["turbidity"], record_data["turbidity"])
        self.assertEqual(data["temperature"], record_data["temperature"])
        self.assertIn("created_at", data)

    def test_add_record_bad_request_missing_field(self):
        """POST /records with missing required field returns 400 Bad Request."""
        incomplete_data = {
            # "location" is omitted
            "ph_level": 7.0,
            "turbidity": 5.0,
            "temperature": 20.0,
        }
        response = self.client.post(
            "/records",
            data=json.dumps(incomplete_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_add_record_bad_request_invalid_json(self):
        """POST /records with invalid JSON format returns 400 Bad Request."""
        invalid_json = "this is not json"
        response = self.client.post(
            "/records",
            data=invalid_json,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class TestRecordsPATCH(BaseTestCase):
    """Tests for PATCH /records/<id> route."""

    def test_update_record_success(self):
        """PATCH /records/<id> successfully updates a record."""
        record_data = {
            "location": "Initial Location",
            "ph_level": 7.0,
            "turbidity": 5.0,
            "temperature": 20.0,
        }
        post_response = self.client.post(
            "/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        update_data = {"location": "Updated Location", "ph_level": 7.5}
        patch_response = self.client.patch(
            f"/records/{record_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(patch_response.status_code, 200)
        updated_record = patch_response.get_json()
        self.assertEqual(updated_record["location"], update_data["location"])
        self.assertEqual(updated_record["ph_level"], update_data["ph_level"])
        self.assertEqual(updated_record["turbidity"], record_data["turbidity"])
        self.assertEqual(updated_record["temperature"], record_data["temperature"])

    def test_update_record_bad_request_invalid_json(self):
        """PATCH /records/<id> with invalid JSON returns 400 Bad Request."""
        record_data = {
            "location": "Initial Location",
            "ph_level": 7.0,
            "turbidity": 5.0,
            "temperature": 20.0,
        }
        post_response = self.client.post(
            "/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        invalid_json = "invalid json"
        patch_response = self.client.patch(
            f"/records/{record_id}",
            data=invalid_json,
            content_type="application/json",
        )
        self.assertEqual(patch_response.status_code, 400)

    def test_update_record_not_found(self):
        """PATCH /records/<id> for a non-existent record returns 404."""
        update_data = {"location": "Updated Location", "ph_level": 7.5}
        patch_response = self.client.patch(
            "/records/999",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(patch_response.status_code, 404)

    def test_update_soft_deleted_record(self):
        """PATCH /records/<id> on a soft-deleted record returns 404."""
        record_data = {
            "location": "Test Location",
            "ph_level": 7.2,
            "turbidity": 4.5,
            "temperature": 18.0,
        }
        post_response = self.client.post(
            "/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        # Soft delete the record first.
        delete_response = self.client.delete(f"/records/{record_id}")
        self.assertEqual(delete_response.status_code, 200)

        # Attempt to update the soft-deleted record.
        update_data = {"location": "Updated After Delete"}
        patch_response = self.client.patch(
            f"/records/{record_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(patch_response.status_code, 404)


class TestRecordsDELETE(BaseTestCase):
    """Tests for DELETE /records/<id> route."""

    def test_delete_record(self):
        """DELETE /records/<id> deletes the record."""
        record_data = {
            "location": "Delete Test",
            "ph_level": 7.0,
            "turbidity": 3.0,
            "temperature": 22.0,
        }
        post_response = self.client.post(
            "/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        delete_response = self.client.delete(f"/records/{record_id}")
        self.assertEqual(delete_response.status_code, 200)
        data = delete_response.get_json()
        self.assertEqual(data["message"], "Record soft-deleted successfully")

        # Verify the record is no longer accessible.
        get_response = self.client.get(f"/records/{record_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_record_not_found(self):
        """DELETE /records/<id> for a non-existent record returns 404."""
        response = self.client.delete("/records/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_already_deleted_record(self):
        """DELETE /records/<id> for a record that has already been soft-deleted returns 404."""
        record_data = {
            "location": "Delete Test",
            "ph_level": 7.0,
            "turbidity": 3.0,
            "temperature": 22.0,
        }
        post_response = self.client.post(
            "/records",
            data=json.dumps(record_data),
            content_type="application/json",
        )
        self.assertEqual(post_response.status_code, 201)

        with self.app.app_context():
            record = Record.query.first()
            record_id = record.id

        # Soft delete the record.
        delete_response = self.client.delete(f"/records/{record_id}")
        self.assertEqual(delete_response.status_code, 200)

        # Attempt to delete again.
        second_delete_response = self.client.delete(f"/records/{record_id}")
        self.assertEqual(second_delete_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
