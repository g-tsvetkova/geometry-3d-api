#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/schemas.py
# Description: marshmallow JSON Schemas for input validation


from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from marshmallow.validate import OneOf
from numpy import array
from app.models.polygon import Polygon3D, Vertex


class PointSchema(Schema):
    points = fields.List(
        fields.List(fields.Float(), validate=validate.Length(equal=3)),
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Points are required."},
    )
    precision = fields.Float(
        missing=1e-7,
        validate=validate.Range(min=0),
        error_messages={"min": "Precision must be non-negative."},
    )


class PolygonSchema(Schema):
    vertices = fields.List(
        fields.Dict(keys=fields.Str(), values=fields.Float()), required=True
    )

    @validates_schema
    def validate_vertices(self, data, **kwargs):
        vertices_data = data["vertices"]

        if len(vertices_data) < 3:
            raise ValidationError(
                "At least three vertices are required to define a polygon."
            )

        # Transform the list of vertex dictionaries to Vertex instances
        vertices = [Vertex(**v) for v in vertices_data]

        # Instantiate a Polygon3D object to validate coplanarity
        try:
            polygon = Polygon3D(vertices)
        except ValueError as e:
            raise ValidationError(str(e))


class MeshSchemaRotation(Schema):
    vertices = fields.List(
        fields.List(fields.Float(), validate=validate.Length(equal=3)),
        required=True,
        description="List of vertices in the mesh.",
    )
    rotation = fields.Dict(
        keys=fields.Str(validate=OneOf(["x", "y", "z"])),
        values=fields.Integer(),
        required=True,
        description="Rotation angles in degrees for the x, y, and z axis.",
    )


class MeshSchemaTranslation(Schema):
    vertices = fields.List(
        fields.List(fields.Float(), validate=validate.Length(equal=3)),
        required=True,
        description="List of vertices in the mesh.",
    )
    translation = fields.Dict(
        keys=fields.Str(validate=OneOf(["x", "y", "z"])),
        values=fields.Float(),
        required=True,
        description="Translation distances along the X, Y, and Z axis.",
    )
