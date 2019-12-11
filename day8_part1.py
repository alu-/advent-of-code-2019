#!/usr/bin/env python3
import textwrap
from collections import OrderedDict

def main():
    with open("./inputs/day8.txt") as file:
        raw_input = file.read()

    width = 25
    height = 6
    layers = make_layers(raw_input, width, height)
    target_layer = find_fewest_zeroes(layers)

    layer_data = "".join(layers[target_layer])
    print(layer_data.count("1") * layer_data.count("2"))


def make_layers(image, width, height):
    layers = OrderedDict()
    current_layer = 1
    layer_lines = 0
    for chunk in textwrap.wrap(image, width):
        if current_layer not in layers:
            layers[current_layer] = []

        layers[current_layer].append(chunk)
        layer_lines += 1
        if layer_lines >= height:
            layer_lines = 0
            current_layer += 1
    return layers


def find_fewest_zeroes(layers):
    zeroes_by_layer = {}
    for layer in layers:
        zeroes_by_layer[layer] = "".join(layers[layer]).count("0")

    return min(zeroes_by_layer, key=zeroes_by_layer.get)


if __name__ == '__main__':
    main()
