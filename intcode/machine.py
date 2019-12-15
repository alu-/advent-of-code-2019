#!/usr/bin/env python3
from enum import Enum
import math
import os

class InstructionException(Exception):
    """ Unhandled instruction """

class Instruction(Enum):
    ADDITION        = 1
    MULTIPLICATION  = 2
    INPUT           = 3
    PRINT           = 4
    JUMP_POSITIVE   = 5
    JUMP_NEGATIVE   = 6
    LESS_THAN       = 7
    EQUALS          = 8
    RELATIVE_ADJUST = 9
    STOP            = 99
    def __get__(self, *args):
        return self.value

class Machine():
    def __init__(self, program, debug=False, interactive=True, stdin=[]):
        self.program = self._parse(program)
        self.extended_memory = {}
        self.relative_offset = 0
        self.debug = debug
        self.interactive = interactive
        self.stdin = stdin
        self.stdout = ""
        self.paused = False
        self.finished = False
        self.pointer = 0

    @staticmethod
    def _parse(program):
        return [int(i) for i in program.rstrip().split(",") if i.replace("-", "").isdigit()]

    def _get_instruction(self, address):
        if address >= len(self.program):
            if self._is_debug():
                print("\tGetting extended memory address {}".format(address))
            try:
                return self.extended_memory[address]
            except KeyError:
                return 0
        else:
            if self._is_debug():
                print("\tGetting value from address {} ({})".format(address, self.program[address]))

            return self.program[address]

    def _set_instruction(self, address, value):
        if address >= len(self.program):
            if self._is_debug():
                print("\tSetting extended memory address {} to {}".format(address, value))

            self.extended_memory[address] = value
        else:
            if self._is_debug():
                print("\tSetting address {} to {}".format(address, value))

            self.program[address] = value

    def _is_debug(self):
        return self.debug

    def _is_interactive(self):
        return self.interactive

    def _set_stdout(self, stdout):
        self.stdout += str(stdout)

    def get_stdout(self):
        out = self.stdout
        self.stdout = ""
        return out

    def _has_input(self):
        return len(self.stdin) > 0

    def _pause_execution(self, state=True):
        self.paused = state

    def _is_paused(self):
        return self.paused

    def is_finished(self):
        return self.finished

    def give_stdin(self, stdin):
        self.stdin.append(stdin)

    def dump_memory(self, heading):
        os.remove("memory.csv")
        memory = self.program
        with open("memory.csv", "a+") as file:
            file.write(str(heading))
            file.write("\n")
            file.write(str(memory))
            file.write("\n\n")

    @staticmethod
    def _get_mode(number, bit):
        characters = [c for i, c in enumerate(reversed(str(number))) if i not in [0, 1]]
        return int(characters[bit]) if len(characters) > bit else 0

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

    def _get_parameter(self, mode, index, write=False):
        if write:
            if mode in [0, 1]:
                return self.program[self.pointer + index]
            elif mode == 2:
                return self.relative_offset + self.program[self.pointer + index]
        else:
            if mode == 0:
                return self._get_instruction(self.program[self.pointer + index])
            elif mode == 1:
                return self.program[self.pointer + index]
            elif mode == 2:
                return self._get_instruction(self.relative_offset + self.program[self.pointer + index])

    def _parameterize_instruction(self, immidiate_instruction):
        instruction = self._last_two_digits(immidiate_instruction)
        if instruction in [
                Instruction.MULTIPLICATION,
                Instruction.ADDITION,
                Instruction.LESS_THAN,
                Instruction.EQUALS
        ]:
            bits = [
                self._get_mode(immidiate_instruction, 0),
                self._get_mode(immidiate_instruction, 1),
                self._get_mode(immidiate_instruction, 2)
            ]
            parameters = [
                self._get_parameter(bits[0], 1),
                self._get_parameter(bits[1], 2),
                self._get_parameter(bits[2], 3, write=True),
            ]
        elif instruction in [Instruction.PRINT, Instruction.RELATIVE_ADJUST]:
            bit = self._get_mode(immidiate_instruction, 0)
            parameters = [self._get_parameter(bit, 1)]
        elif instruction in [Instruction.JUMP_POSITIVE, Instruction.JUMP_NEGATIVE]:
            bits = [
                self._get_mode(immidiate_instruction, 0),
                self._get_mode(immidiate_instruction, 1)
            ]
            parameters = [
                self._get_parameter(bits[0], 1),
                self._get_parameter(bits[1], 2)
            ]
        elif instruction is Instruction.INPUT:
            bit = self._get_mode(immidiate_instruction, 0)
            parameters = [self._get_parameter(bit, 1, write=True)]
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
                if self._is_interactive():
                    self._set_instruction(parameters[0], int(input("Please give an input: ")))
                else:
                    if not self._has_input():
                        if self._is_debug():
                            print("Halted execution")
                        return self._pause_execution()
                    else:
                        stdin = self.stdin[0]
                        del self.stdin[0]
                        self._set_instruction(parameters[0], stdin)
            elif instruction is Instruction.PRINT:
                if self._is_interactive():
                    print(parameters[0])
                else:
                    self._set_stdout(parameters[0])
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
            elif instruction is Instruction.RELATIVE_ADJUST:
                if self._is_debug():
                    print("\tAdjusting relative from {} to {}".format(
                        self.relative_offset, self.relative_offset + parameters[0])
                    )

                self.relative_offset += parameters[0]
            else:
                raise InstructionException(
                    "Unknown value {} while iterating address {}".format(instruction, self.pointer)
                )

            self.pointer += len(parameters) + 1
            if self.pointer > len(self.program):
                raise StopIteration("Program ran outside memory bounds at address {}".format(self.pointer))

        self.finished = True
        return self
