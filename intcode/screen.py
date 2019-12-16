#!/usr/bin/env python3
import itertools
import curses

from enum import Enum
from collections import defaultdict


class Tiles(Enum):
    EMPTY  = 0
    WALL   = 1
    BLOCK  = 2
    PADDLE = 3
    BALL   = 4

    def getTexture(self):
        textures = {
            0: "",
            1: "|",
            2: "█",
            3: "▁",
            4: "o"
        }
        return textures[self.value]

class Screen():
    def __init__(self, vm):
        self.vm = vm
        self.vm.set_interactive(False)
        self.output_buffer = defaultdict(lambda: {})
        self.automatic = False
        self.score = 0

    def run(self, interactive=True):
        if interactive:
            curses.wrapper(self._run_loop)
            print(self.score)
        else:
            self._run_and_parse_output()

    def _run_loop(self, stdscr):
        stdscr.refresh()
        key = None
        while True:
            if key == "q":
                break
            elif key == "a":
                self.automatic = True
            elif key in ["KEY_LEFT", "KEY_RIGHT"]:
                self.vm.give_stdin(-1 if key == "KEY_LEFT" else 1)
            elif key == "KEY_UP":
                self.vm.give_stdin(0)

            self._run_and_parse_output()

            key = self.render(stdscr)

            if self.vm.is_finished():
                break

    def _run_and_parse_output(self):
        self.vm.run()
        if self.vm.has_stdout():
            output = self.vm.get_stdout().split(",")
            for chunk in chunks(output, 3):
                self.output_buffer[int(chunk[0])][int(chunk[1])] = int(chunk[2])

    def get_output_buffer(self):
        return self.output_buffer

    def render(self, stdscr):
        key = None
        width = len(self.output_buffer)
        height = max([len(x) for x in self.output_buffer.values()])
        info_box = curses.newwin(7, width + 2, height + 5 , 0)
        win = curses.newwin(height + 2, width + 2, 0, 0)
        score = curses.newwin(3, 25, height + 2, 0)

        info_box.addstr(1, 1, "Controls:")
        info_box.addstr(2, 1, "LEFT and RIGHT to move paddles.")
        info_box.addstr(3, 1, "UP to advance the ball one position.")
        info_box.addstr(4, 1, "q to quit.")
        info_box.addstr(5, 1, "a for automatic mode.")

        info_box.box()
        win.box()
        score.box()
        while True:
            stdscr.erase()
            if self.automatic:
                paddle_position = 0
                ball_position = 0
                for x, r in self.output_buffer.items():
                    if x == -1:
                        continue
                    for y, tile in r.items():
                        if Tiles(tile) is Tiles.PADDLE:
                            paddle_position = x

                        if Tiles(tile) is Tiles.BALL:
                            ball_position = x

                key = "KEY_UP"
                if ball_position > paddle_position:
                    key = "KEY_RIGHT"
                elif ball_position < paddle_position:
                    key = "KEY_LEFT"
            else:
                stdscr.refresh()

            for x, r in self.output_buffer.items():
                for y, tile in r.items():
                    if x == -1:
                        score.addstr(1, 1, "Score: {}".format(tile))
                        self.score = tile
                        continue

                    win.addstr(y + 1, x + 1, Tiles(tile).getTexture())

            info_box.refresh()
            win.refresh()
            score.refresh()

            if not self.automatic:
                key = stdscr.getkey()

            if key in ["KEY_LEFT", "KEY_RIGHT", "KEY_UP", "a", "q"]:
                return key
            else:
                info_box.box()
                win.box()
                score.box()
                stdscr.erase()


def chunks(iterable, size):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, size))
