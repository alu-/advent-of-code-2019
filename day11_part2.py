#!/usr/bin/env python3
from enum import Enum
from collections import defaultdict

from intcode.machine import Machine

class Robot():
    class Color(Enum):
        black = 0
        white = 1
        def __get__(self, *args):
            return self.value

    class Direction(Enum):
        up    = 0
        right  = 1
        down  = 2
        left = 3
        def __get__(self, *args):
            return self.value

    def __init__(self, name):
        self.name = name
        self.hull = defaultdict(lambda: self.Color.black)
        self.hull[(0,0)] = self.Color.black
        self.coordinates = (0, 0)
        self.facing = self.Direction.up

    def handle_instruction(self, i):
        self.paint(int(i[0]))
        self.rotate(int(i[1]))
        self.move(int(i[1]))

    def paint(self, color):
        self.hull[self.coordinates] = color

    def rotate(self, i):
        self.facing = self.Direction((self.facing + (-1 if i == 0 else 1)) % len(self.Direction)).value

    def move(self, i):
        if self.facing is self.Direction.up:
            self.coordinates = (self.coordinates[0], self.coordinates[1] + 1)
        elif self.facing is self.Direction.right:
            self.coordinates = (self.coordinates[0] + 1, self.coordinates[1])
        elif self.facing is self.Direction.down:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 1)
        elif self.facing is self.Direction.left:
            self.coordinates = (self.coordinates[0] - 1, self.coordinates[1])

    def read_current_position(self):
        return self.hull[self.coordinates]

    def get_hull(self):
        return self.hull

    def get_output(self):
        return self.read_current_position()

    def print_board(self):
        lowest_x = None
        lowest_y = None
        highest_x = None
        highest_y = None

        for coord in self.hull:
            if lowest_x is None:
                lowest_x = coord[0]
            if lowest_y is None:
                lowest_y = coord[1]

            if highest_x is None:
                highest_x = coord[0]
            if highest_y is None:
                highest_y = coord[1]

            if coord[0] < lowest_x:
                lowest_x = coord[0]
            if coord[1] < lowest_y:
                lowest_y = coord[1]

            if coord[0] > highest_x:
                highest_x = coord[0]
            if coord[1] > highest_y:
                highest_y = coord[1]

        for x in (range(lowest_x, highest_x + 1)):
            for y in range(lowest_y, highest_y + 1) :
                if self.hull[(x, y)] == 0:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()


def main():
    with open("./inputs/day11.txt") as file:
        raw_input = file.read()

    vm = Machine(raw_input, interactive=False, stdin=[1])
    mr = Robot("Elliot")
    while not vm.is_finished():
        robot_output = mr.get_output()
        vm.give_stdin(robot_output)
        vm.run()
        machine_output = vm.get_stdout()
        mr.handle_instruction(machine_output)

    mr.print_board()


if __name__ == '__main__':
    main()
