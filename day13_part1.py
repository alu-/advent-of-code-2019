#!/usr/bin/env python3
from intcode.machine import Machine
from intcode.screen import Screen


def main():
    with open("./inputs/day13.txt") as file:
        raw_input = file.read()

    vm = Machine(raw_input)
    screen = Screen(vm)
    screen.run()
    output = screen.get_output_buffer()

    glyphs = []
    for x, r in output.items():
        for y, c in r.items():
            glyphs.append(c)

    print(glyphs.count(2))

if __name__ == '__main__':
    main()
