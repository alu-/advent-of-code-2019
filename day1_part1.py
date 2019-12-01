#!/usr/bin/env python3
from math import floor


def main():
    with open("./inputs/day1.txt") as f:
        lines = f.read().splitlines()

    answer = 0
    for l in lines:
        fuel = floor(int(l) / 3) - 2
        answer += fuel

    print(answer)


if __name__ == '__main__':
    main()
