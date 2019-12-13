#!/usr/bin/env python3
from enum import Enum
from math import atan2, degrees, sqrt
from collections import OrderedDict


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
    center, _ = find_best_position_and_score(asteroids)
    position_data = sort_positions_by_angles(find_positions_from_origin(center[0], center[1], asteroids))
    bet_asteroid = destroy_asteroids(position_data, 200)
    print((bet_asteroid['y'] * 100) + bet_asteroid['x'])


def find_best_position_and_score(asteroids):
    highest_score = 0
    best_position = ()
    for asteroid in asteroids:
        positions = find_positions_from_origin(asteroid[0], asteroid[1], asteroids)
        score = get_score_from_positions(positions)
        if score > highest_score:
            highest_score = score
            best_position = asteroid

    return best_position, highest_score


def find_positions_from_origin(origin_x, origin_y, asteroids):
    position_data = []
    for asteroid in asteroids:
        if asteroid[0] == origin_x and asteroid[1] == origin_y:
            continue

        angle = atan2((asteroid[1] - origin_y), (asteroid[0] - origin_x))
        position_data.append({
            'x' : asteroid[0],
            'y' : asteroid[1],
            'degrees': '{0:.5f}'.format(degrees(angle)),
            'distance': sqrt(((origin_x - asteroid[0]) ** 2) + ((origin_y - asteroid[1]) ** 2))
        })

    return position_data


def get_score_from_positions(asteroids):
    by_angles = {}
    for asteroid in asteroids:
        if asteroid['degrees'] not in by_angles:
            by_angles[asteroid['degrees']] = []
        by_angles[asteroid['degrees']].append(asteroid)

    return len(by_angles)


def sort_positions_by_angles(asteroids):
    by_angles = {}
    for asteroid in asteroids:
        if asteroid['degrees'] not in by_angles:
            by_angles[asteroid['degrees']] = []
        by_angles[asteroid['degrees']].append(asteroid)

    for angle, items in by_angles.items():
        by_angles[angle] = sorted(items, key=lambda k: k['distance'])

    ordered_dict = OrderedDict()
    angles = sorted(by_angles.keys(), key=float, reverse=True)
    for angle in angles:
        ordered_dict[angle] = by_angles[angle]

    return ordered_dict


def destroy_asteroids(positions, target=200):
    pop_count = 0
    while positions:
        for k in list(positions.keys()):
            pop = positions[k].pop(0)
            if pop:
                pop_count += 1
                if pop_count == target:
                    return pop

            if not positions[k]:
                del positions[k]


if __name__ == '__main__':
    main()
