#!/usr/bin/env python3
from intcode.machine import Machine
from intcode.screen import Screen


def main():
    with open("./inputs/day13.txt") as file:
        raw_input = file.read()

    raw_input = "2{}".format(raw_input[1:])

    vm = Machine(raw_input)
    screen = Screen(vm)
    screen.run(interactive=True)


if __name__ == '__main__':
    main()
