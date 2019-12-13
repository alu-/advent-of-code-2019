#!/usr/bin/env python3
from enum import Enum
from math import atan2, degrees, sqrt


class Map(Enum):
    ASTEROID    = "#"
    EMPTY_SPACE = "."
    def __get__(self, *args):
        return self.value


def main():
    with open("./inputs/day10.txt") as file:
        raw_input = file.read().splitlines()

    starmap = list(map(list, raw_input))
    scores = {}
    for x, row in enumerate(starmap):
        for y, cell in enumerate(row):
            if cell is Map.ASTEROID:
                if not x in scores:
                    scores[x] = {}
                scores[x].update({y: find_score(x, y, raw_input)})

    highest_score = 0
    for x, r in scores.items():
        for y, a in r.items():
            if len(a) > highest_score:
                highest_score = len(a)

    print(highest_score)


def find_score(origin_x, origin_y, starmap):
    position_data = []
    for x, row in enumerate(starmap):
        for y, cell in enumerate(row):
            if x == origin_x and y == origin_y:
                continue

            if cell is Map.ASTEROID:
                angle = atan2((y - origin_y), (x - origin_x))
                position_data.append({
                    'name': '{},{}'.format(x, y),
                    'degrees': '{0:.5f}'.format(degrees(angle)),
                    'distance': sqrt( ((origin_x-x)**2)+((origin_y-y)**2) )
                })

    return filter_blocked_asteroids(position_data)


def filter_blocked_asteroids(asteroids):
    by_angles = {}
    for a in asteroids:
        if a['degrees'] not in by_angles:
            by_angles[a['degrees']] = []
        by_angles[a['degrees']].append(a)

    filter_asteroids = []
    for _, a in by_angles.items():
        for asteroid in a:
            for other_asteroid in a:
                if asteroid['name'] == other_asteroid['name']:
                    continue

                if asteroid['distance'] > other_asteroid['distance']:
                    if asteroid['name'] not in filter_asteroids:
                        filter_asteroids.append(asteroid['name'])
                else:
                    if other_asteroid['name'] not in filter_asteroids:
                        filter_asteroids.append(other_asteroid['name'])

    return [a for a in asteroids if not a['name'] in filter_asteroids]


def display_map(starmap, score=None):
    for x, row in enumerate(starmap):
        for y, cell in enumerate(row):
            if x in score and y in score[x]:
                print(len(score[x][y]), end="")
            else:
                print(cell, end="")
        print()


if __name__ == '__main__':
    main()
