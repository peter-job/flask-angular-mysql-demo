import datetime as dt

from flask import Blueprint, jsonify, request

from api import db
from api.water_quality.models import Record
from api.water_quality.schemas import RecordSchema

record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

bp = Blueprint("water-quality", __name__, url_prefix="/water-quality")
"""Blueprint for water quality API routes."""


@bp.route("/records", methods=["GET"])
def get_records():
    "GET /water-quality/records - Return all records that haven't been soft-deleted."
    records = Record.query.filter(Record.deleted_at.is_(None)).all()
    return jsonify(records_schema.dump(records))


@bp.route("/records", methods=["POST"])
def create_record():
    "POST /water-quality/records - Create a new record."
    data = request.get_json()
    new_record = Record(
        location=data["location"],
        ph_level=data["ph_level"],
        turbidity=data["turbidity"],
        temperature=data["temperature"],
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify(record_schema.dump(new_record)), 201


@bp.route("/records/<int:record_id>", methods=["GET"])
def get_record(record_id):
    "GET /water-quality/records/<id> - Return a single record if it hasn't been soft-deleted."
    record = Record.query.filter(
        Record.id == record_id, Record.deleted_at.is_(None)
    ).first_or_404()
    return jsonify(record_schema.dump(record))


@bp.route("/records/<int:record_id>", methods=["PATCH"])
def update_record(record_id):
    """PATCH /water-quality/records/<id> - Update an existing record (only if not soft-deleted)."""
    record = Record.query.filter(
        Record.id == record_id, Record.deleted_at.is_(None)
    ).first_or_404()
    data = request.get_json()

    # Update only fields provided in the request payload.
    if "location" in data:
        record.location = data["location"]
    if "ph_level" in data:
        record.ph_level = data["ph_level"]
    if "turbidity" in data:
        record.turbidity = data["turbidity"]
    if "temperature" in data:
        record.temperature = data["temperature"]

    db.session.commit()
    return jsonify(record_schema.dump(record))


@bp.route("/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    "DELETE /water-quality/records/<id> - Soft delete a record by setting its deleted_at timestamp."
    record = Record.query.filter(
        Record.id == record_id, Record.deleted_at.is_(None)
    ).first_or_404()
    record.deleted_at = dt.datetime.now(dt.timezone.utc)
    db.session.commit()
    return jsonify({"message": "Record soft-deleted successfully"})
