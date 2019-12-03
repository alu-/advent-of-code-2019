#!/usr/bin/env python3
from math import floor


def main():
    with open("./inputs/day1.txt") as file:
        lines = file.read().splitlines()

    answer = 0
    for line in lines:
        fuel = floor(int(line) / 3) - 2
        answer += fuel

    print(answer)


if __name__ == '__main__':
    main()
