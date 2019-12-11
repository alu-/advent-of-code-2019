#!/usr/bin/env python3
import networkx as nx


def main():
    with open("./inputs/day6.txt") as file:
        raw_input = file.read().splitlines()

    graph = nx.DiGraph()
    for edge in raw_input:
        graph.add_edge(*edge.split(")"))

    length = nx.single_source_shortest_path_length(graph, "COM")
    print(sum(length.values()))


if __name__ == '__main__':
    main()
