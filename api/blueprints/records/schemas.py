from marshmallow import EXCLUDE, Schema, fields, post_dump


class RecordSchema(Schema):
    id = fields.Int(strict=True, dump_only=True)
    location = fields.Str(required=True)
    ph_level = fields.Number(required=True)
    turbidity = fields.Number(required=True)
    temperature = fields.Number(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE

    @post_dump
    def remove_none_fields(self, data, **kwargs):
        """Remove fields with None values from the serialized output."""
        return {key: value for key, value in data.items() if value is not None}
