#!/usr/bin/env python3
from collections import OrderedDict
from enum import Enum
from day8_part1 import make_layers

class Colors(Enum):
    BLACK       = "0"
    WHITE       = "1"
    TRANSPARENT = "2"
    def __get__(self, *args):
        return self.value

def main():
    with open("./inputs/day8.txt") as file:
        raw_input = file.read()

    width = 25
    height = 6
    image = {}
    layers = OrderedDict(reversed(list(make_layers(raw_input, width, height).items())))
    for layer, rows in layers.items():
        image[layer] = []
        for row_index, row in enumerate(rows):
            colored_row = ""
            for pixel_index, pixel in enumerate(row):

                if pixel is Colors.BLACK:
                    colored_row += " "
                elif pixel is Colors.WHITE:
                    colored_row += "▀"
                elif pixel is Colors.TRANSPARENT:
                    try:
                        colored_row += image[layer+1][row_index][pixel_index]
                    except KeyError:
                        colored_row += " "

            image[layer].append(colored_row)

    for pixel in image[1]:
        print(pixel)


if __name__ == '__main__':
    main()
