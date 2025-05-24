#!/usr/bin/env python
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
import argparse
import json
import math
import wynncraft_waypoint_utils as utils
from wynncraft_waypoint_utils import Box, Location

def main():
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
    parser.add_argument(
        '--filter-box',
        nargs=6,
        type=int,
        dest='filter_box',
    )
    parser.add_argument(
        '--sort-radial',
        nargs=3,
        type=int,
        dest='sort_radial',
    )
    parser.add_argument(
        '--sort-alphanumeric',
        action='store_true',
        dest='sort_alphanumeric',
    )
    parser.add_argument(
        '--invert-sort',
        action='store_true',
        dest='invert_sort',
    )
    args = parser.parse_args()

    waypoints = []

    # read input files
    for file in args.input:
        waypoints.extend(json.load(file))

    # Radius based filtering
    if args.filter_radius != 0:
        radius = args.filter_radius[0]
        print(f'Filtering waypoints within {radius} blocks of distance')

        filtered_waypoints = []
        matches = 0

        for i, waypoint in enumerate(waypoints, 1):
            location = Location.from_wynntils_waypoint(waypoint)
            match_found = False
            for other_waypoint in waypoints[i:]:
                other_location = Location.from_wynntils_waypoint(waypoint)
                dst = location.distance_to(other_location)

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

    # Box based filtering
    if args.filter_box is not None:
        bound1 = Location.from_tuple(args.filter_box[:3])
        bound2 = Location.from_tuple(args.filter_box[3:])
        box = Box(bound1, bound2)
        print(f'Filtering waypoints within box {box}')

        waypoints = [
            waypoint for waypoint in waypoints
            if box.contains(Location.from_wynntils_waypoint(waypoint))
        ]
        print(f'{len(waypoints)} matches found')

    # Radius sorting
    if args.sort_radial is not None:
        center = Location.from_tuple(args.sort_radial)
        print(f'Sorting waypoints by distance to {center}')
        waypoints.sort(
            key=lambda x: Location.from_wynntils_waypoint(x).distance_to(center),
        )

    # Alphanumeric sorting
    if args.sort_alphanumeric:
        print(f'Sorting waypoints by name')
        waypoints.sort(key=lambda x: x["name"])

    # Invert sort
    if args.invert_sort:
        print(f'Inverting waypoint order')
        waypoints = list(reversed(waypoints))

    # write output to file
    json.dump(waypoints, args.output, indent=2)

if __name__ == "__main__":
    main()
