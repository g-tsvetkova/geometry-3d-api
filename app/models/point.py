#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/models/mesh.py
# Description: Point model definition


class Point:
    def __init__(self, identifier, x, y, z):
        super().__init__(identifier)
        self.x = x
        self.y = y
        self.z = z
