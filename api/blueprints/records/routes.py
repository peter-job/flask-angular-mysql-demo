import datetime as dt

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from api import db

from .models import Record
from .schemas import RecordSchema

record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

bp = Blueprint("records", __name__)
"""Blueprint for water quality records API routes."""


@bp.route("/records", methods=["GET"])
def get_records():
    "GET /records - Return all records that haven't been soft-deleted."
    records = Record.query.filter(Record.deleted_at.is_(None)).all()
    return jsonify(records_schema.dump(records))


@bp.route("/records", methods=["POST"])
def create_record():
    "POST /records - Create a new record."
    data = request.get_json()
    if data is None:
        return jsonify({"message": "No input data provided"}), 400
    try:
        validated_data = record_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_record = Record(**validated_data)
    db.session.add(new_record)
    db.session.commit()
    return jsonify(record_schema.dump(new_record)), 201


@bp.route("/records/<int:record_id>", methods=["GET"])
def get_record(record_id):
    "GET /records/<id> - Return a single record if it hasn't been soft-deleted."
    record = Record.query.filter(
        Record.id == record_id, Record.deleted_at.is_(None)
    ).first_or_404()
    return jsonify(record_schema.dump(record))


@bp.route("/records/<int:record_id>", methods=["PATCH"])
def update_record(record_id):
    """PATCH /records/<id> - Update an existing record (only if not soft-deleted)."""
    record = Record.query.filter(
        Record.id == record_id, Record.deleted_at.is_(None)
    ).first_or_404()
    data = request.get_json()
    if data is None:
        return jsonify({"message": "No input data provided"}), 400
    try:
        validated_data = record_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in validated_data.items():
        setattr(record, key, value)
    db.session.commit()
    return jsonify(record_schema.dump(record))


@bp.route("/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    "DELETE /records/<id> - Soft delete a record by setting its deleted_at timestamp."
    record = Record.query.filter(
        Record.id == record_id, Record.deleted_at.is_(None)
    ).first_or_404()
    record.deleted_at = dt.datetime.now(dt.timezone.utc)
    db.session.commit()
    return jsonify({"message": "Record soft-deleted successfully"})
