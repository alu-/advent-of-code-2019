#!/usr/bin/env python3
from functools import reduce

def main():
    with open("./inputs/day3.txt") as file:
        lines = parse_input(file.read())

    coordinates = []
    for line in lines:
        coordinates.append(plot(line))

    intersections = calculate_intersections(coordinates)
    print(get_shortest_distance(intersections))


def parse_input(raw_input):
    return [line.split(",") for line in raw_input.splitlines()]


def plot(line):
    """ Plot path from origin 0, 0 """
    path = [(0, 0)]
    for instruction in line:
        direction = instruction[:1]
        steps = int(instruction[1:])
        path = path + resolve_path(direction, steps, path[-1])
    return path


def resolve_path(direction, steps, start):
    # TODO: would be cool to make this a generator
    path = []
    if direction == "L":
        # TODO: refactor away duplicate code
        for step in range(1, steps + 1):
            step = start[0] - step
            coordinate = (step, start[1])
            path.append(coordinate)
    elif direction == "R":
        for step in range(1, steps + 1):
            step = start[0] + step
            coordinate = (step, start[1])
            path.append(coordinate)
    elif direction == "U":
        for step in range(1, steps + 1):
            step = start[1] + step
            coordinate = (start[0], step)
            path.append(coordinate)
    elif direction == "D":
        for step in range(1, steps + 1):
            step = start[1] - step
            coordinate = (start[0], step)
            path.append(coordinate)
    return path


def calculate_intersections(lists):
    return list(reduce(set.intersection, [set(item) for item in lists]))


def get_shortest_distance(intersections):
    lowest_distance = None
    for intersection in intersections:
        distance = abs(intersection[0]) + abs(intersection[1])
        if distance == 0:
            continue

        if lowest_distance is None or distance < lowest_distance:
            lowest_distance = distance

    return lowest_distance


if __name__ == '__main__':
    main()
