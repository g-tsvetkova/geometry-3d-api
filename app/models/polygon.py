#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/models/polygon.py
# Description: Polygon model definition

import numpy as np


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y, self.z - other.z)

    def cross(self, other):
        return Vertex(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


class Polygon3D:
    def __init__(self, vertices):
        super().__init__()
        if len(vertices) < 3:
            raise ValueError(
                "At least three vertices are required to define a polygon."
            )
        self.vertices = vertices
        if not self.are_coplanar():
            raise ValueError("The vertices do not lie on the same plane.")

    def are_coplanar(self):
        normal = (self.vertices[1] - self.vertices[0]).cross(
            self.vertices[2] - self.vertices[0]
        )
        for vertex in self.vertices[3:]:
            if not np.isclose((vertex - self.vertices[0]).dot(normal), 0):
                return False
        return True

    def is_convex(self):
        if len(self.vertices) < 4:
            return True  # A triangle is always convex

        def sign(x):
            return (x > 0) - (x < 0)

        normal = (self.vertices[1] - self.vertices[0]).cross(
            self.vertices[2] - self.vertices[0]
        )
        initial_sign = None

        for i in range(len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            v3 = self.vertices[(i + 2) % len(self.vertices)]

            cross_product = (v2 - v1).cross(v3 - v2)
            current_sign = sign(cross_product.dot(normal))

            if initial_sign is None:
                initial_sign = current_sign
            elif current_sign != initial_sign:
                return False

        return True
