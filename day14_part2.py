#!/usr/bin/env python3
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

    ore_to_make_one_fuel, _ = recurse_compounds(chemicals, chemicals['FUEL'], 1)

    target = 10**12
    minimum = 1
    maximum = int((target / ore_to_make_one_fuel) * 1.5)
    highest = {}
    while minimum < maximum:
        current = maximum + (minimum - maximum) // 2
        lowest,  _ = recurse_compounds(chemicals, chemicals['FUEL'], minimum)
        middle,  _ = recurse_compounds(chemicals, chemicals['FUEL'], current)

        if lowest <= target:
            highest[minimum] = lowest
        if middle <= target:
            highest[current] = middle

        if middle >= target:
            maximum = current - 1
        elif middle > lowest and middle <= target:
            minimum = current + 1
        else:
            maximum = current - 1

    print(max(highest))


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
