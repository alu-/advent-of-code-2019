#!/usr/bin/env python3
import re

from math import ceil


class Chemical():
    def __init__(self, name: str, amount: int, compounds: list = []):
        self.name = name
        self.amount = int(amount)
        self.compounds = compounds


def main() -> None:
    with open("./inputs/day14.txt") as file:
        raw_input = file.read().splitlines()

    chemicals = {}
    for line in raw_input:
        chemical = parse_line(line)
        chemicals[chemical.name] = chemical

    answer, _ = recurse_compounds(chemicals, chemicals['FUEL'], 1)
    print(answer)


def parse_line(line: str) -> Chemical:
    left, right = line.split(" => ")
    amount, name = right.split(" ")
    compounds = parse_compounds(left)

    return Chemical(name, amount, compounds)


def parse_compounds(data: str) -> list:
    line = [d for d in data.split(", ")]
    compounds = []
    for l in line:
        amount, name = l.split(" ")
        compounds.append(Chemical(name, amount, []))

    return compounds


def recurse_compounds(chemicals: list, target: Chemical, amount: int, bucket: dict = {}) -> tuple:
    result = 0
    for compound in target.compounds:
        if compound.name == "ORE":
            multiplier = ceil(amount / target.amount)
            trailing_compounds = (multiplier * target.amount) - amount
            if trailing_compounds > 0:
                bucket[target.name] = (trailing_compounds if not target.name in bucket else bucket[target.name] + trailing_compounds)

            return compound.amount * multiplier, bucket

        compound_required_amount = compound.amount * int((amount / target.amount))
        if compound.name in bucket:
            bucket_amount = min(bucket[compound.name], compound_required_amount)
            compound_required_amount -= bucket_amount
            bucket[compound.name] = bucket[compound.name] - bucket_amount
            if bucket[compound.name] == 0:
                del bucket[compound.name]

        multiplier = ceil(compound_required_amount / chemicals[compound.name].amount)
        new_amount = chemicals[compound.name].amount * multiplier
        if new_amount == 0:
            continue

        recurse_amount, bucket = recurse_compounds(chemicals, chemicals[compound.name], new_amount, bucket)
        result += recurse_amount

        trailing_compounds = new_amount - compound_required_amount
        if trailing_compounds > 0:
            if compound.name in bucket:
                bucket[compound.name] = bucket[compound.name] + trailing_compounds
            else:
                bucket[compound.name] = trailing_compounds

    return result, bucket


if __name__ == '__main__':
    main()
