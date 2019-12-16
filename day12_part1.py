#!/usr/bin/env python3
import re

from collections import OrderedDict
from itertools import permutations
from functools import lru_cache

import vectormath as vmath


def main():
    with open("./inputs/day12.txt") as file:
        raw_input = file.read()

    names = ["Io", "Europa", "Ganymede", "Callisto"]
    moons = OrderedDict()
    matches = re.findall(r"^<x=(-*\d+), y=(-*\d+), z=(-*\d+)>$", raw_input, re.MULTILINE)
    for match in matches:
        moons[names.pop(0)] = {
            'position': vmath.Vector3(int(match[0]), int(match[1]), int(match[2])),
            'velocity': vmath.Vector3(0, 0, 0)
        }

    for step in range(1, 1001):
        gravity = calculate_gravity(moons)
        moons = apply_gravity(moons, gravity)
        moons = apply_velocities(moons)

        if step == 1000:
            moons = calculate_energies(moons)
            print(int(sum([x['energy'] for _, x in moons.items()])))


def calculate_gravity(moons):
    moon_pairs = get_moon_pairs(tuple(moons.keys()))
    gravity = {name: [] for name in moons}
    for pair in moon_pairs:
        gravity[pair[0]].append(
            vmath.Vector3(get_velocity(moons[pair[0]]['position'].x, moons[pair[1]]['position'].x), 0, 0)
        )
        gravity[pair[1]].append(
            vmath.Vector3(get_velocity(moons[pair[1]]['position'].x, moons[pair[0]]['position'].x), 0, 0)
        )

        gravity[pair[0]].append(
            vmath.Vector3(0, get_velocity(moons[pair[0]]['position'].y, moons[pair[1]]['position'].y), 0)
        )
        gravity[pair[1]].append(
            vmath.Vector3(0, get_velocity(moons[pair[1]]['position'].y, moons[pair[0]]['position'].y), 0)
        )

        gravity[pair[0]].append(
            vmath.Vector3(0, 0, get_velocity(moons[pair[0]]['position'].z, moons[pair[1]]['position'].z))
        )
        gravity[pair[1]].append(
            vmath.Vector3(0, 0, get_velocity(moons[pair[1]]['position'].z, moons[pair[0]]['position'].z))
        )

    return gravity


def get_velocity(x, y):
    if x > y:
        return -1
    elif x < y:
        return 1
    else:
        return 0


def apply_gravity(moons, gravity):
    for name in moons.keys():
        for x in gravity[name]:
            moons[name]['velocity'] += x

    return moons


def apply_velocities(moons):
    for name in moons.keys():
        moons[name]['position'] += moons[name]['velocity']
    return moons


@lru_cache(maxsize=1)
def get_moon_pairs(moons):
    moon_pairs = permutations(moons, 2)
    return {tuple(item) for item in map(sorted, moon_pairs)}


def calculate_energies(moons):
    for name in moons.keys():
        moons[name]['potential_energy'] = sum(abs(moons[name]['position']))
        moons[name]['kinetic_energy'] = sum(abs(moons[name]['velocity']))
        moons[name]['energy'] = moons[name]['potential_energy'] * moons[name]['kinetic_energy']

    return moons


if __name__ == '__main__':
    main()
