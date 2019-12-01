#!/usr/bin/env python3
from math import floor


def main():
    with open("./inputs/day1.txt") as f:
        lines = f.read().splitlines()

    answer = 0
    for l in lines:
        answer += calculate_fuel_for_mass(int(l))

    print(answer)


def calculate_fuel_for_mass(mass, total_fuel=0):
    fuel = floor(mass / 3) - 2
    if fuel <= 0:
        return total_fuel

    total_fuel += fuel
    return calculate_fuel_for_mass(fuel, total_fuel)


if __name__ == '__main__':
    main()
