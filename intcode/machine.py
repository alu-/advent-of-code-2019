#!/usr/bin/env python3
from enum import Enum
import math
import os

class InstructionException(Exception):
    """ Unhandled instruction """

class Instruction(Enum):
    ADDITION       = 1
    MULTIPLICATION = 2
    INPUT          = 3
    PRINT          = 4
    JUMP_POSITIVE  = 5
    JUMP_NEGATIVE  = 6
    LESS_THAN      = 7
    EQUALS         = 8
    STOP           = 99
    def __get__(self, *args):
        return self.value

class Machine():
    def __init__(self, program, debug=False):
        self.program = self._parse(program)
        self.debug = debug
        self.pointer = 0

    @staticmethod
    def _parse(program):
        return [int(i) for i in program.rstrip().split(",") if i.replace("-", "").isdigit()]

    def _get_instruction(self, address):
        if self._is_debug():
            print("\tGetting value from address {} ({})".format(address, self.program[address]))
        return self.program[address]

    def _set_instruction(self, address, value):
        if self._is_debug():
            print("\tSetting address {} to {}".format(address, value))

        self.program[address] = value

    def _is_debug(self):
        return self.debug

    def dump_memory(self, heading):
        os.remove("memory.csv")
        memory = self.program
        with open("memory.csv", "a+") as file:
            file.write(str(heading))
            file.write("\n")
            file.write(str(memory))
            file.write("\n\n")

    @staticmethod
    def _is_bit_set(number, bit):
        try:
            return str(number)[:-2][::-1][bit-1] == "1"
        except IndexError:
            return False

    @staticmethod
    def _get_integer_length(integer):
        return int(math.log10(integer)) + 1

    def _is_immidiate_mode(self, instruction):
        if self._get_integer_length(instruction) > 1:
            return str(instruction)[:1] == "1"

        return False

    @staticmethod
    def _last_two_digits(number):
        return abs(number) % 100

    def _parameterize_instruction(self, immidiate_instruction):
        instruction = self._last_two_digits(immidiate_instruction)
        if instruction in [
                Instruction.MULTIPLICATION,
                Instruction.ADDITION,
                Instruction.LESS_THAN,
                Instruction.EQUALS
        ]:
            bits = [
                self._is_bit_set(immidiate_instruction, 1),
                self._is_bit_set(immidiate_instruction, 2)
            ]
            parameters = [
                self._get_instruction(self.program[self.pointer + 1]) if not bits[0]
                else self.program[self.pointer + 1],
                self._get_instruction(self.program[self.pointer + 2]) if not bits[1]
                else self.program[self.pointer + 2],
                self.program[self.pointer + 3]
            ]
        elif instruction is Instruction.PRINT:
            bit = self._is_bit_set(immidiate_instruction, 1)
            parameters = [
                self._get_instruction(self.program[self.pointer + 1]) if not bit
                else self.program[self.pointer + 1],
            ]
        elif instruction in [Instruction.JUMP_POSITIVE, Instruction.JUMP_NEGATIVE]:
            bits = [
                self._is_bit_set(immidiate_instruction, 1),
                self._is_bit_set(immidiate_instruction, 2)
            ]
            parameters = [
                self._get_instruction(self.program[self.pointer + 1]) if not bits[0]
                else self.program[self.pointer + 1],
                self._get_instruction(self.program[self.pointer + 2]) if not bits[1]
                else self.program[self.pointer + 2]
            ]
        elif instruction is Instruction.INPUT:
            parameters = [self.program[self.pointer + 1]]
        else:
            raise InstructionException("Unknown instruction {}".format(immidiate_instruction))

        return instruction, parameters

    def run(self): #pylint:disable=too-many-branches
        if not self.program:
            return

        while self.program[self.pointer] is not Instruction.STOP:
            instruction = self.program[self.pointer]
            instruction, parameters = self._parameterize_instruction(instruction)

            if self._is_debug():
                print("{}: {}({}) {}".format(
                    self.pointer, Instruction(instruction).name, self.program[self.pointer], parameters
                ))

            if instruction is Instruction.ADDITION:
                if self._is_debug():
                    print("\t{} + {} = {}".format(parameters[0], parameters[1], parameters[0] + parameters[1]))
                self._set_instruction(parameters[2], parameters[0] + parameters[1])
            elif instruction is Instruction.MULTIPLICATION:
                if self._is_debug():
                    print("\t{} * {} = {}".format(parameters[0], parameters[1], parameters[0] * parameters[1]))
                self._set_instruction(parameters[2], parameters[0] * parameters[1])
            elif instruction is Instruction.INPUT:
                self._set_instruction(parameters[0], int(input("Please give an input: ")))
            elif instruction is Instruction.PRINT:
                print(parameters[0])
            elif instruction is Instruction.JUMP_POSITIVE:
                if parameters[0]:
                    if self._is_debug():
                        print("\tJumping to instruction address {}".format(parameters[1]))

                    self.pointer = parameters[1]
                    continue
                else:
                    if self._is_debug():
                        print("\tParameter false, not jumping to address {}".format(parameters[1]))
            elif instruction is Instruction.JUMP_NEGATIVE:
                if not parameters[0]:
                    if self._is_debug():
                        print("\tJumping to instruction address {}".format(parameters[1]))

                    self.pointer = parameters[1]
                    continue
                else:
                    if self._is_debug():
                        print("\tParameter true, not jumping to address {}".format(parameters[1]))
            elif instruction is Instruction.LESS_THAN:
                if self._is_debug():
                    print("\t{} < {} == {}".format(parameters[0], parameters[1], int(parameters[0] < parameters[1])))

                self._set_instruction(parameters[2], int(parameters[0] < parameters[1]))
            elif instruction is Instruction.EQUALS:
                if self._is_debug():
                    print("\t{} == {} == {}".format(parameters[0], parameters[1], int(parameters[0] < parameters[1])))

                self._set_instruction(parameters[2], int(parameters[0] == parameters[1]))
            else:
                raise InstructionException(
                    "Unknown value {} while iterating address {}".format(instruction, self.pointer)
                )

            if self._is_debug():
                print()

            self.pointer += len(parameters) + 1
            if self.pointer > len(self.program):
                raise StopIteration("Program ran outside memory bounds at address {}".format(self.pointer))
