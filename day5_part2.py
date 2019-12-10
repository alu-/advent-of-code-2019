#!/usr/bin/env python3
from intcode.machine import Machine

def main():
    with open("./inputs/day5.txt") as file:
        raw_input = file.read()

    vm = Machine(raw_input)
    vm.run()


if __name__ == '__main__':
    main()
