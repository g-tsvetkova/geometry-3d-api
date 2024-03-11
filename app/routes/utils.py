#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/utils.py
# Description: Helper functions for 3D geometry operations

import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as R


class Hull3D:
    """
    Class to calculate the convex hull of a set of
    3D points and check if they are coplanar or
    collinear.
    """

    def __init__(self, points, precision=1e-7):
        self.points = points
        self.precision = precision
        self.convex_hull = ConvexHull(points)
        self.is_coplanar = self.check_coplanarity()
        self.is_collinear = self.check_colinearity()

    def get_vertices(self):
        return self.points[self.convex_hull.vertices]

    def check_coplanarity(self):
        return np.isclose(self.convex_hull.volume, 0, atol=self.precision)

    def check_colinearity(self):
        if not self.is_coplanar:
            return False
        line_vec = self.get_vertices()[1] - self.get_vertices()[0]
        projections = [
            np.dot(p - self.get_vertices()[0], line_vec) / np.linalg.norm(line_vec)
            for p in self.get_vertices()
        ]
        return np.var(projections) < self.precision


class BoundingBox3D:
    """
    Class to calculate the volume of a 3D bounding box
    """

    def __init__(self, points, is_coplanar=False, is_collinear=False):
        self.points = points
        self.is_coplanar = is_coplanar
        self.is_collinear = is_collinear

    def calculate_volume(self):
        if self.is_collinear:
            lengths = np.max(self.points, axis=0) - np.min(self.points, axis=0)
            return np.max(lengths)
        elif self.is_coplanar:
            min_bound = np.min(self.points, axis=0)
            max_bound = np.max(self.points, axis=0)
            return np.prod(max_bound - min_bound[:2])
        else:
            min_bound = np.min(self.points, axis=0)
            max_bound = np.max(self.points, axis=0)
            return np.prod(max_bound - min_bound)


class RotationOptimizer:
    def __init__(self, hull):
        self.hull = hull

    def objective_function(self, rotation_angles):
        if self.hull.is_collinear or self.hull.is_coplanar:
            bounding_box = BoundingBox3D(
                self.hull.get_vertices(), self.hull.is_coplanar, self.hull.is_collinear
            )
            volume = bounding_box.calculate_volume()
            return volume
        else:
            rotation = R.from_euler("xyz", rotation_angles, degrees=True)
            rotated_points = rotation.apply(self.hull.get_vertices())
            bounding_box = BoundingBox3D(rotated_points)
            return bounding_box.calculate_volume()

    def find_optimal_rotation(self):
        initial_guess = [0, 0, 0]
        result = minimize(self.objective_function, initial_guess, method="SLSQP")
        return result


def define_plane(p1, p2, p3):
    """Calculate the plane defined by three points."""
    v1 = p2 - p1
    v2 = p3 - p1
    cp = np.cross(v1, v2)
    a, b, c = cp
    d = -np.dot(cp, p1)
    return a, b, c, d


def point_in_plane(point, coeffs):
    """Check if a point lies in the plane defined by the given coefficients."""
    a, b, c, d = coeffs
    return np.isclose(a * point[0] + b * point[1] + c * point[2] + d, 0)


def is_convex_3d(points):
    """Check if a 3D polygon defined by a list of points is convex."""
    cross_product_signs = []
    for i in range(len(points)):
        p1 = np.array(points[i])
        p2 = np.array(points[(i + 1) % len(points)])
        p3 = np.array(points[(i + 2) % len(points)])
        edge1 = p2 - p1
        edge2 = p3 - p2
        cross_product = np.cross(edge1, edge2)
        cross_product_sign = np.sign(np.dot(cross_product, cross_product))
        cross_product_signs.append(cross_product_sign)
    return all(sign == cross_product_signs[0] for sign in cross_product_signs)


def all_points_in_one_plane(points):
    """Check if all points of a polygon are coplanar."""
    p1, p2, p3 = np.array(points[0]), np.array(points[1]), np.array(points[2])
    plane_coeffs = define_plane(p1, p2, p3)
    return all(point_in_plane(np.array(point), plane_coeffs) for point in points[3:])
