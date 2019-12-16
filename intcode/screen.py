#!/usr/bin/env python3
import itertools

from enum import Enum
from collections import defaultdict


class Tiles(Enum):
    EMPTY  = 0
    WALL   = 1
    BLOCK  = 2
    PADDLE = 3
    BALL   = 4

class Screen():
    def __init__(self, vm):
        self.vm = vm
        self.vm.set_interactive(False)
        self.output_buffer = defaultdict(lambda: {})

    def run(self):
        self.vm.run()
        output = self.vm.get_stdout().split(",")

        for chunk in chunks(output, 3):
            self.output_buffer[int(chunk[0])][int(chunk[1])] = int(chunk[2])

    def get_output_buffer(self):
        return self.output_buffer


def chunks(iterable, size):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, size))
