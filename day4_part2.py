#!/usr/bin/env python3
import re

def main():
    with open("./inputs/day4.txt") as file:
        raw_input = file.read().strip()

    possible_passwords = get_possible_passwords(raw_input)
    print(sum(1 for _ in possible_passwords))


def get_possible_passwords(interval):
    interval = list(map(int, interval.split("-")))
    interval[1] += 1
    for number in range(*interval):
        if length_is_not_six(number):
            continue

        if not has_adjacent_digits(number):
            continue

        if has_decreasing_digits(number):
            continue

        if has_adjacent_digit_group(number):
            continue

        yield number


def length_is_not_six(number):
    return len(str(number)) != 6


def has_adjacent_digits(number):
    # TODO: This is probably obsolete now that we have has_adjacent_digit_group
    previous_digit = None
    for digit in str(number):
        if previous_digit is not None and previous_digit == digit:
            return True
        previous_digit = digit

    return False


def has_decreasing_digits(number):
    previous_digit = None
    for digit in str(number):
        if previous_digit is not None and previous_digit > digit:
            return True
        previous_digit = digit

    return False


def has_adjacent_digit_group(number):
    matches = re.findall(r"(([0-9])\2{1,})", str(number))
    for match in matches:
        if len(match[0]) == 2:
            return False

    return True


if __name__ == '__main__':
    main()
