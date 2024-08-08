#!/usr/bin/env python
# Copyright 2024 Christoph Matthias Kohnen
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
import argparse
import json
import math

parser = argparse.ArgumentParser(description='Wynncraft Waypoint Utils')
parser.add_argument(
    '--input',
    required=True,
    nargs='+',
    type=argparse.FileType('rt'),
    dest='input',
)
parser.add_argument(
    '--output',
    required=True,
    type=argparse.FileType('wt'),
    dest='output',
)
parser.add_argument(
    '--verbose',
    action='store_true',
    dest='verbose',
)
parser.add_argument(
    '--filter-radius',
    nargs=1,
    type=float,
    default=0,
    dest='filter_radius',
)
args = parser.parse_args()


def waypoint_location_tuple(waypoint: dict) -> tuple[int, int, int]:
    location_dict = waypoint['location']
    return tuple(location_dict[key] for key in ('x', 'y', 'z'))


def waypoint_distance(
    waypoint1: tuple[int, int, int],
    waypoint2: tuple[int, int, int],
) -> float:
    vector = (b - a for a, b in zip(waypoint1, waypoint2))
    return math.sqrt(sum(i*i for i in vector))


waypoints = []

# read input files
for file in args.input:
    waypoints.extend(json.load(file))


# Radius based filtering
if args.filter_radius[0]:
    radius = args.filter_radius[0]
    print(f'Filtering waypoints within {radius} blocks of distance')

    filtered_waypoints = []
    matches = 0

    for i, waypoint in enumerate(waypoints, 1):
        location = waypoint_location_tuple(waypoint)
        match_found = False
        for other_waypoint in waypoints[i:]:
            other_location = waypoint_location_tuple(other_waypoint)
            dst = waypoint_distance(location, other_location)

            if dst > radius:
                continue
            match_found = True
            matches += 1
            if args.verbose:
                print(f'found match: {location} -> {other_location}'
                      f' ({dst:0.2f} blocks distance)')
            break

        if not match_found:
            filtered_waypoints.append(waypoint)

    if matches:
        waypoints = filtered_waypoints
        print(f'Found {matches} matches.')

# write output to file
json.dump(waypoints, args.output, indent=2)
