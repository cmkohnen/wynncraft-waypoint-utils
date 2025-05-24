# Copyright 2024-2025 Christoph Matthias Kohnen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

class Location:

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_tuple(cls, tuple_: tuple):
        return cls(*tuple_)

    @classmethod
    def from_wynntils_waypoint(cls, waypoint: dict):
        location_dict = waypoint['location']
        return cls.from_tuple(location_dict[key] for key in ('x', 'y', 'z'))

    @classmethod
    def from_string(cls, string: str):
        string = string.replace('`', '').replace(',', '')
        return cls.from_tuple(string.split(" "))

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __str__(self) -> str:
        return f'(x={self.x}, y={self.y}, z={self.z})'

    def as_tuple(self) -> tuple:
        return tuple(self.x, self.y, self.z)

    def as_dict(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }

    def distance_to(self, other) -> float:
        vector = (b - a for a, b in zip(self, other))
        return math.sqrt(sum(i * i for i in vector))


class Box:

    def __init__(self, a: Location = None, b: Location = None):
        if a is None:
            a = Location()
        if b is None:
            b = Location()
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f'(a={self.a}, b={self.b})'

    def contains(self, location: Location) -> bool:
        return all(i <= max(a, b) and i >= min(a, b)
                   for i, a, b in zip(location, a, b))

class Sphere:

    def __init__(self, center: Location = None, r: float = 0):
        if center is None:
            center = Location()
        self.center = center
        self.r = r

    def __str__(self) -> str:
        return f'(center={self.center}, r={self.r})'

    def contains(self, location: Location) -> bool:
        return self.center.distance_to(location) <= self.r
