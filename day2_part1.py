#!/usr/bin/env python3

def main():
    with open("./inputs/day2.txt") as f:
        input = f.read()

    instructions = parse_intcode_into_instructions(input)
    mutated_instructions = run_instructions(instructions)
    print(get_answer(mutated_instructions))


def parse_intcode_into_instructions(raw_body):
    body = restore_state([int(i) for i in raw_body.rstrip().split(",") if i.isdigit()])
    instructions = []
    while body:
        if body[0] == 99:
            instructions.append([99])
            body = body[1:]
        else:
            instructions.append(body[:4])
            body = body[4:]

    return instructions


def restore_state(state):
    state[1] = 12
    state[2] = 2
    return state


def run_instructions(instructions):
    for x in range(0, len(instructions)):
        instruction = instructions[x]
        opcode = instruction[0]
        if opcode == 1:
            x = get_instruction_value_at_address(instructions, instruction[1])
            y = get_instruction_value_at_address(instructions, instruction[2])
            instructions = set_instruction_value_at_address(instructions, x + y, instruction[3])
        elif opcode == 2:
            x = get_instruction_value_at_address(instructions, instruction[1])
            y = get_instruction_value_at_address(instructions, instruction[2])
            instructions = set_instruction_value_at_address(instructions, x * y, instruction[3])
        elif opcode == 99:
            return instructions
        else:
            raise ValueError("Unhandled opcode: {}".format(opcode))


def get_instruction_value_at_address(instructions, address):
    return [item for sublist in instructions for item in sublist][address]


def set_instruction_value_at_address(instructions, value, address):
    address_counter = 0
    for i, instruction in enumerate(instructions):
        for p, position in enumerate(instruction):
            if address_counter == address:
                instructions[i][p] = value
                return instructions
            address_counter += 1

    return instructions


def get_answer(instructions):
    return instructions[0][0]


if __name__ == '__main__':
    main()
