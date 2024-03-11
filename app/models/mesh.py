#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/models/mesh.py
# Description: Mesh3D model definition

import numpy as np


class Mesh3D:
    def __init__(self, vertices):
        """
        Initialize the Mesh3D object with vertices.
        :param vertices: A numpy array of vertices, shape (n, 3), where n is the number of vertices.
        """
        self.vertices = np.array(vertices)

    def rotate_x(self, degrees):
        """
        Rotate the mesh around the X-axis by a certain degree.
        :param degrees: The rotation angle in degrees.
        """
        radians = np.radians(degrees)
        rotation_matrix = np.array(
            [
                [1, 0, 0],
                [0, np.cos(radians), -np.sin(radians)],
                [0, np.sin(radians), np.cos(radians)],
            ]
        )
        self.vertices = np.dot(self.vertices, rotation_matrix)

    def rotate_y(self, degrees):
        """
        Rotate the mesh around the Y-axis by a certain degree.
        :param degrees: The rotation angle in degrees.
        """
        radians = np.radians(degrees)
        rotation_matrix = np.array(
            [
                [np.cos(radians), 0, np.sin(radians)],
                [0, 1, 0],
                [-np.sin(radians), 0, np.cos(radians)],
            ]
        )
        self.vertices = np.dot(self.vertices, rotation_matrix)

    def rotate_z(self, degrees):
        """
        Rotate the mesh around the Z-axis by a certain degree.
        :param degrees: The rotation angle in degrees.
        """
        radians = np.radians(degrees)
        rotation_matrix = np.array(
            [
                [np.cos(radians), -np.sin(radians), 0],
                [np.sin(radians), np.cos(radians), 0],
                [0, 0, 1],
            ]
        )
        self.vertices = np.dot(self.vertices, rotation_matrix)

    def translate(self, a, b, c):
        """
        Translate the mesh by a, b, and c units along the X, Y, and Z axis respectively.
        :param a: Translation along the X axis.
        :param b: Translation along the Y axis.
        :param c: Translation along the Z axis.
        """
        translation_matrix = np.array([a, b, c])
        self.vertices += translation_matrix
