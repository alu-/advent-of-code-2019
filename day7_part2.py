#!/usr/bin/env python3
from itertools import permutations
from intcode.machine import Machine


def main():
    with open("./inputs/day7.txt") as file:
        raw_input = file.read()

    outputs = {}
    for permutation in permutations('56789', 5):
        vms = []
        for perm in permutation:
            vms.append(Machine(raw_input, interactive=False, stdin=[int(perm)]))

        input_signal = 0
        while True:
            done = True
            for machine in vms:
                machine.give_stdin(input_signal)
                machine.run()
                input_signal = int(machine.get_stdout())
                if not machine.is_finished():
                    done = False

            if done:
                outputs[input_signal] = permutation
                break

    print(max(outputs))


if __name__ == '__main__':
    main()
