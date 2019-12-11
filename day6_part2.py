#!/usr/bin/env python3
import networkx as nx


def main():
    with open("./inputs/day6.txt") as file:
        raw_input = file.read().splitlines()

    graph = nx.Graph()
    for edge in raw_input:
        graph.add_edge(*edge.split(")"))

    print(nx.shortest_path_length(graph, "YOU", "SAN") - 3)


if __name__ == '__main__':
    main()
