#!/usr/bin/env python3
from itertools import permutations
from intcode.machine import Machine


def main():
    with open("./inputs/day7.txt") as file:
        raw_input = file.read()

    outputs = {}
    for permutation in permutations('01234', 5):
        input_signal = 0
        for perm in permutation:
            input_signal = int(
                Machine(raw_input, interactive=False, stdin=[int(perm), input_signal]).run().get_stdout()
            )
        outputs[input_signal] = permutation

    print(max(outputs))

if __name__ == '__main__':
    main()
