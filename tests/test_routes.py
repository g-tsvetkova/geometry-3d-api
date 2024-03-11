import unittest
import json
from app import create_app


class GeometryAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            print(self.app.url_map)

        self.rotation_data = {
            "rotation": {"x": 30, "y": 45, "z": 60},
            "vertices": [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        }

        self.translation_data = {
            "translation": {"x": 10, "y": 20, "z": 30},
            "vertices": [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        }

        self.wrong_data = {
            "rotation": {"x": 30, "y": "not a number", "z": 60},
            "vertices": [[0, 1, 2], [3, 4], [6, 7, 8]],
        }

    def test_rotate_mesh_success(self):
        response = self.client.post(
            "/api/v1/meshes/rotation",
            data=json.dumps(self.rotation_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_rotate_mesh_failure(self):
        response = self.client.post(
            "/api/v1/meshes/rotation",
            data=json.dumps(self.wrong_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_translate_mesh_success(self):
        response = self.client.post(
            "/api/v1/meshes/translation",
            data=json.dumps(self.translation_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_translate_mesh_failure(self):
        response = self.client.post(
            "/api/v1/meshes/translation",
            data=json.dumps(self.wrong_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_polygon_convexity_check(self):
        data = {"vertices": [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]}
        response = self.client.get(
            "/api/v1/polygons/is-convex-polygon",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
