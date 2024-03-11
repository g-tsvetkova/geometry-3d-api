#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/mesh/routes.py
# Description: Routes for the mesh endpoints

from flask import request, jsonify
from app.models.mesh import Mesh3D
from app.schemas import MeshSchemaRotation, MeshSchemaTranslation
from flask import Blueprint
from marshmallow import ValidationError

bp_meshes = Blueprint("meshes", __name__, url_prefix="/api/v1/meshes")


@bp_meshes.route("/rotation", methods=["POST"])
def rotate_mesh():
    """
    Rotate a 3D mesh around the X, Y, or Z axis by a certain degree.
    ---
    tags:
      - meshes
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Input data for rotating a mesh
        schema:
          type: object
          required:
            - vertices
          properties:
            vertices:
              type: array
              items:
                type: array
                items:
                  type: number
                  format: float
              description: Array of vertex coordinates, each vertex is a list of three floats representing the x, y, and z coordinates.
            rotation:
              type: object
              properties:
                x:
                  type: integer
                  description: Rotation angle around the X-axis in degrees.
                y:
                  type: integer
                  description: Rotation angle around the Y-axis in degrees.
                z:
                  type: integer
                  description: Rotation angle around the Z-axis in degrees.
              additionalProperties: false
              description: Rotation angles in degrees for each specified axis.
    responses:
      200:
        description: The rotated vertices of the mesh.
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
      400:
        description: Invalid input data.
    """

    # {
    #   "rotation": {"x": 30, "y": 45, "z": 60},
    #   "vertices": [[x1, y1, z1], [x2, y2, z2], ...]
    # }
    json_input = request.get_json()
    try:
        data = MeshSchemaRotation().load(json_input)
        mesh = Mesh3D(data["vertices"])
        rotation = data.get("rotation")
        # if rotation:
        #     mesh.rotate(
        #         rotation
        #     )  # Assuming your Mesh3D class has a rotate method that takes a dictionary
        if rotation:
            if "x" in rotation:
                mesh.rotate_x(rotation["x"])
            if "y" in rotation:
                mesh.rotate_y(rotation["y"])
            if "z" in rotation:
                mesh.rotate_z(rotation["z"])

            return jsonify({"vertices": mesh.vertices.tolist()}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_meshes.route("/translation", methods=["POST"])
def translate_mesh():
    """
    Translate a 3D mesh by units along the X, Y, and Z axis.
    ---
    tags:
      - meshes
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Input data for translating a mesh
        schema:
          type: object
          required:
            - vertices
            - translation
          properties:
            vertices:
              type: array
              description: Array of vertex coordinates.
              items:
                type: object
                required:
                  - x
                  - y
                  - z
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
            translation:
              type: object
              description: Translation distances along the X, Y, and Z axis.
              required:
                - x
                - y
                - z
              properties:
                x:
                  type: number
                  description: Translation distance along the X-axis.
                y:
                  type: number
                  description: Translation distance along the Y-axis.
                z:
                  type: number
                  description: Translation distance along the Z-axis.
    responses:
      200:
        description: The translated vertices of the mesh.
        schema:
          type: object
          properties:
            vertices:
              type: array
              items:
                type: object
                required:
                  - x
                  - y
                  - z
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
      400:
        description: Invalid input data.
    """
    mesh_schema = MeshSchemaTranslation()
    try:
        data = mesh_schema.load(request.get_json())
        mesh = Mesh3D(data["vertices"])
        translation = data.get("translation")
        if translation:
            mesh.translate(*translation.values())
        return jsonify({"vertices": mesh.vertices.tolist()})
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred."}), 500
