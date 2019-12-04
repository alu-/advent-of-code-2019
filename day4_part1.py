#!/usr/bin/env python3

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

        yield number


def length_is_not_six(number):
    return len(str(number)) != 6


def has_adjacent_digits(number):
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


if __name__ == '__main__':
    main()
