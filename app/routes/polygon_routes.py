#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/polygons/routes.py
# Description: Routes for the polygons API

from flask import Blueprint, request, jsonify
from app.schemas import PolygonSchema
from marshmallow import ValidationError
from app.models.polygon import Polygon3D, Vertex

bp_polygons = Blueprint("polygons", __name__, url_prefix="/api/v1/polygons")


@bp_polygons.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"error": error.messages}), 400


@bp_polygons.route("/is-convex-polygon", methods=["POST"])
def check_polygon_convexity():
    """
    Checks if a polygon in 3D space is convex.
    ---
    tags:
      - polygons
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Input data for checking polygon convexity
        schema:
          type: object
          required:
            - vertices
          properties:
            vertices:
              type: array
              items:
                type: object
                properties:
                  x:
                    type: number
                    format: float
                  y:
                    type: number
                    format: float
                  z:
                    type: number
                    format: float
              description: "Array of 3D vertices."
    responses:
      200:
        description: The convexity of the polygon.
        schema:
          type: object
          properties:
            is_convex:
              type: boolean
              description: "True if the polygon is convex, False otherwise."
      400:
        description: Bad request. The input data is invalid.
        schema:
          type: object
          properties:
            error:
              type: string
              description: "Error message."
    """
    try:
        json_input = request.get_json()
        validated_data = PolygonSchema().load(json_input)

        # Assuming the conversion to Polygon3D happens within the schema validation,
        # simply reconstruct the polygon from the validated data for clarity
        vertices = [Vertex(v["x"], v["y"], v["z"]) for v in validated_data["vertices"]]
        polygon = Polygon3D(vertices)

        return jsonify({"is_convex": polygon.is_convex()}), 200
    except ValidationError as err:
        return handle_validation_error(err)
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred."}), 500
