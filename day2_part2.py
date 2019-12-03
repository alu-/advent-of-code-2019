#!/usr/bin/env python3

def main():
    with open("./inputs/day2.txt") as file:
        raw_input = file.read()

    number_of_instructions = len([int(i) for i in raw_input.rstrip().split(",") if i.isdigit()])
    for noun in range(0, number_of_instructions):
        for verb in range(0, number_of_instructions):
            instructions = parse_intcode_into_instructions(raw_input, noun, verb)
            mutated_instructions = run_instructions(instructions)
            answer = get_answer(mutated_instructions)
            if answer == 19690720:
                print(100 * noun + verb)
                exit()


def parse_intcode_into_instructions(raw_body, noun, verb):
    body = restore_state([int(i) for i in raw_body.rstrip().split(",") if i.isdigit()], noun, verb)
    instructions = []
    while body:
        if body[0] == 99:
            instructions.append([99])
            body = body[1:]
        else:
            instructions.append(body[:4])
            body = body[4:]

    return instructions


def restore_state(state, noun, verb):
    state[1] = noun
    state[2] = verb
    return state


def run_instructions(instructions):
    for index, _ in enumerate(instructions):
        instruction = instructions[index]
        opcode = instruction[0]
        if opcode == 1:
            new_value = get_instruction_value_at_address(
                instructions, instruction[1]
            ) + get_instruction_value_at_address(
                instructions, instruction[2]
            )
            instructions = set_instruction_value_at_address(instructions, new_value, instruction[3])
        elif opcode == 2:
            new_value = get_instruction_value_at_address(
                instructions, instruction[1]
            ) * get_instruction_value_at_address(
                instructions, instruction[2]
            )
            instructions = set_instruction_value_at_address(instructions, new_value, instruction[3])
        elif opcode == 99:
            return instructions
        else:
            raise ValueError("Unhandled opcode: {}".format(opcode))

    return []


def get_instruction_value_at_address(instructions, address):
    return [item for sublist in instructions for item in sublist][address]


def set_instruction_value_at_address(instructions, value, address):
    address_counter = 0
    for line_index, instruction in enumerate(instructions):
        for position_index, _ in enumerate(instruction):
            if address_counter == address:
                instructions[line_index][position_index] = value
                return instructions
            address_counter += 1

    return instructions


def get_answer(instructions):
    return instructions[0][0]


if __name__ == '__main__':
    main()
