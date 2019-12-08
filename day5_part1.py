#!/usr/bin/env python3

def main():
    with open("./inputs/day5.txt") as file:
        raw_input = file.read()

    instructions = parse_intcode_into_instructions(raw_input)
    mutated_instructions = run_instructions(instructions)


def parse_intcode_into_instructions(raw_body):
    body = [int(i) for i in raw_body.rstrip().split(",") if i.replace("-", "").isdigit()]
    instructions = []
    while body:
        if body[0] == 99:
            instructions.append([99])
            body = body[1:]
        elif body[0] == 3:
            instructions.append(body[:2])
            body = body[2:]
        elif body[0] == 4:
            instructions.append(body[:2])
            body = body[2:]
        elif str(body[0])[:1] == "1" or body[0] == 1:
            parameters = len(str(body[0])) - 2 + 1
            opcode = str(body[0])[-1:]
            if opcode == "3" or opcode == "4":
                parameters = 2
            elif opcode == "0" or opcode == "1" or opcode == "2":
                parameters = 4
            else:
                parameters = 1

            instructions.append(body[:parameters])
            body = body[parameters:]
        else:
            instructions.append(body[:4])
            body = body[4:]

    return instructions


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
        elif opcode == 3:
            instructions = set_instruction_value_at_address(instructions, ask_for_input(), instruction[1])
        elif opcode == 4:
            print(get_instruction_value_at_address(instructions, instruction[1]))
        elif opcode == 99:
            return instructions
        elif str(opcode)[:1] == "1":
            instructions = handle_immidiate_mode(instructions, instruction)
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


def handle_immidiate_mode(instructions, instruction):
    opcode = str(instruction[0]).zfill(5)
    operation = opcode[-1]
    parameters = []

    modes = reversed(opcode[:len(opcode)-2])
    for index, mode in enumerate(modes):
        if index >= len(instruction) - 1:
            break

        if index == 2:
            parameters.append(instruction[index + 1])
        elif mode == "0":
            # position mode
            parameters.append(get_instruction_value_at_address(instructions, instruction[index + 1]))
        else:
            # immediate mode
            parameters.append(instruction[index + 1])

    if operation == "1":
        new_value = parameters[0] + parameters[1]
        instructions = set_instruction_value_at_address(instructions, new_value, parameters[2])
    elif operation == "2":
        product = parameters[0] * parameters[1]
        instructions = set_instruction_value_at_address(instructions, product, parameters[2])
    elif operation == "3":
        instructions = set_instruction_value_at_address(instructions, ask_for_input(), parameters[2])
    elif operation == "4":
        print(get_instruction_value_at_address(instructions, parameters[0]))
    else:
        raise ValueError("Unhandled opcode: {}".format(opcode))

    return instructions


def ask_for_input():
    return int(input("Input? "))


if __name__ == '__main__':
    main()
