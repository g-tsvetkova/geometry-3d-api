#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/points/routes.py
# Description: Routes for the points endpoint

from flask import Blueprint
from ..schemas import PointSchema
from .utils import Hull3D, BoundingBox3D, RotationOptimizer
from flask import request, jsonify
from app.schemas import PointSchema
from marshmallow import ValidationError
from numpy import array


bp_points = Blueprint("points", __name__, url_prefix="/api/v1/points")


@bp_points.route("/convex-hull", methods=["POST"])
def get_convex_hull():
    """
    Calculate the convex hull of a set of 3D points.
    ---
    tags:
      - points
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Input data for calculating the convex hull
        schema:
          type: object
          required:
            - points
          properties:
            points:
              type: array
              items:
                type: array
                items:
                  type: number
                  format: float
              description: "Array of 3D points."
    responses:
      200:
        description: The vertices of the convex hull.
        schema:
          type: object
          properties:
            vertices:
              type: array
              items:
                type: array
                items:
                  type: number
                  format: float
          description: "Array of 3D points."
      400:
        description: Bad request. The input data is invalid.
        schema:
          type: object
          properties:
            messages:
              type: object
              description: "Error messages."
    """
    json_input = request.get_json()
    schema = PointSchema()
    try:
        data = schema.load(json_input)
    except ValidationError as err:
        return jsonify(err.messages), 400

    points = array(data["points"])
    hull = Hull3D(points)
    convex_hull_vertices = hull.get_vertices()
    return jsonify({"vertices": convex_hull_vertices.tolist()})


@bp_points.route("/bounding-box", methods=["POST"])
def get_bounding_box_data():
    """
    Calculate the bounding box of a set of 3D points
    by first finding convex hull and then optimizes
    the rotation of the bounding box.

    Inspired by Chang, C. T., Gorissen, B., & Melchior, S. (2011).
    Fast oriented bounding box optimization on the rotation group SO (3, ℝ).
    ACM Transactions on Graphics (TOG), 30(5), 1-16.

    ---
    tags:
      - points
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          description: Input data for calculating the bounding box
          schema:
            type: object
            required:
              - points
            properties:
              points:
                type: array
                items:
                    type: array
                    items:
                      type: number
                      format: float
                description: "Array of 3D points."
    responses:
      200:
        description: The vertices of the bounding box.
        schema:
          type: object
          properties:
            vertices:
              type: array
              items:
                type: array
                items:
                  type: number
                  format: float
          description: "Array of 3D points."
      400:
        description: Bad request. The input data is invalid.
        schema:
          type: object
          properties:
            messages:
              type: object
              description: "Error messages."
    """
    json_input = request.get_json()
    schema = PointSchema()
    try:
        data = schema.load(json_input)
    except ValidationError as err:
        return jsonify(err.messages), 400

    points = array(data["points"])
    precision = data["precision"]

    hull = Hull3D(points, precision=precision)
    optimizer = RotationOptimizer(hull)
    result = optimizer.find_optimal_rotation()

    return jsonify(
        {
            "optimal_rotation_angles_degrees": result.x.tolist(),
            "minimal_volume": result.fun,
            "precision_used": precision,
        }
    )
