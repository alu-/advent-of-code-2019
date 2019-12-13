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

    starmap = map(list, raw_input)
    asteroids = [(x, y) for x, r in enumerate(starmap) for y, a in enumerate(r) if a == Map.ASTEROID]
    _, score = find_best_position_and_score(asteroids)
    print(score)


def find_best_position_and_score(asteroids):
    highest_score = 0
    best_position = ()
    for asteroid in asteroids:
        score = find_score(asteroid[0], asteroid[1], asteroids)
        if score > highest_score:
            highest_score = score
            best_position = asteroid

    return best_position, highest_score


def find_score(origin_x, origin_y, asteroids):
    position_data = []
    for asteroid in asteroids:
        if asteroid[0] == origin_x and asteroid[1] == origin_y:
            continue

        angle = atan2((asteroid[1] - origin_y), (asteroid[0] - origin_x))
        position_data.append({
            'name': '{},{}'.format(asteroid[0], asteroid[1]),
            'degrees': '{0:.5f}'.format(degrees(angle)),
            'distance': sqrt(((origin_x - asteroid[0]) ** 2) + ((origin_y - asteroid[1]) ** 2))
        })

    return count_angles(position_data)


def count_angles(asteroids):
    by_angles = {}
    for asteroid in asteroids:
        if asteroid['degrees'] not in by_angles:
            by_angles[asteroid['degrees']] = []
        by_angles[asteroid['degrees']].append(asteroid)

    return len(by_angles)


if __name__ == '__main__':
    main()
