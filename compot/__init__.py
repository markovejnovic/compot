#!/usr/bin/env python

import curses
from dataclasses import dataclass
from typing import Any, Tuple
from enum import IntEnum

__VERSION__ = '0.2.0'


@dataclass
class Measurement:
    """Represents a Measurement of an object in terms of ``w``idth and
    ``h``eight in characters.
    """
    w: int
    h: int

    @staticmethod
    def inf():
        return Measurement(int(1e6), int(1e6))


class LayoutSpec(IntEnum):
    """The LayoutSpec determines how widgets should behave.

    ``FIT_CONTENT`` hints to a widget to minimize its area to fit the content.
    ``FILL`` hints to a widget to use up all the offered area. ``EXACT`` is
    unused.
    """
    FIT_CONTENT = 0
    FILL = 1
    EXACT = 2


class MeasurementSpec(tuple):
    """A ``MeasurementSpec`` is a poorly named class represeting a curses
    position of an object. Usually, you don't need to use this directly as all
    your widgets will handle it themselves.
    """
    @staticmethod
    def INJECTED():
        return MeasurementSpec.xywh(0, 0, 0, 0)

    @property
    def y(self):
        return self[2]

    @property
    def x(self):
        return self[3]

    @property
    def h(self):
        return self[0]

    @property
    def w(self):
        return self[1]

    @property
    def curses(self):
        return (self.h, self.w, self.y, self.x)

    @staticmethod
    def xywh(x: int, y: int, w: int, h: int) -> 'MeasurementSpec':
        return MeasurementSpec((h, w, y, x))

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.w}, {self.h})'


class Colors:
    """This enum defines all functional colors used in the program."""
    OK = 8
    WARNING = 9
    ERROR = 10
    BG = 11
    FG = 12


    @staticmethod
    def __rgb2curses(r: int, g: int, b: int) -> Tuple[int, int, int]:
        c = 1000 / 255
        return tuple(int(c * x) for x in (r, g, b))

    @staticmethod
    def init_curses():
        if curses.can_change_color():
            ic = curses.init_color
            ic(Colors.OK, *Colors.__rgb2curses(80, 250, 123))
            ic(Colors.WARNING, *Colors.__rgb2curses(255, 184, 108))
            ic(Colors.ERROR, *Colors.__rgb2curses(255, 85, 85))
            ic(Colors.BG, *Colors.__rgb2curses(40, 42, 54))
            ic(Colors.FG, *Colors.__rgb2curses(248, 248, 242))
            return

        curses.use_default_colors()
        Colors.OK = curses.COLOR_GREEN
        Colors.WARNING = curses.COLOR_YELLOW
        Colors.ERROR = curses.COLOR_RED
        Colors.BG = 0
        Colors.FG = curses.COLOR_WHITE

class ColorPairs(IntEnum):
    """This function defines all the curses.ColorPair exposed to the
    program.

    Colors are defined in terms of their functional purpose.
    """
    INFO = 8
    OK = 9
    WARNING = 10
    ERROR = 11

    INFO_INVERTED = 28
    OK_INVERTED = 29
    WARNING_INVERTED = 30
    ERROR_INVERTED = 31

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'

    @property
    def inverse(self) -> 'ColorPairs':
        """Returns the inverse of a color pair."""
        return ColorPairs(self.value + 20)

    @staticmethod
    def get(color: 'ColorPairs') -> int:
        """Returns the target color for curses."""
        return curses.color_pair(color)

    @staticmethod
    def init_curses():
        """Exposes all the defined colors to curses."""
        curses.init_pair(ColorPairs.OK_INVERTED, Colors.BG, Colors.OK)
        curses.init_pair(ColorPairs.WARNING_INVERTED,
                         Colors.FG, Colors.WARNING)
        curses.init_pair(ColorPairs.ERROR_INVERTED, Colors.FG, Colors.ERROR)
        curses.init_pair(ColorPairs.INFO_INVERTED, Colors.BG, Colors.FG)
        curses.init_pair(ColorPairs.INFO, Colors.FG, Colors.BG)
        curses.init_pair(ColorPairs.OK, Colors.OK, Colors.BG)
        curses.init_pair(ColorPairs.WARNING, Colors.WARNING, Colors.BG)
        curses.init_pair(ColorPairs.ERROR, Colors.ERROR, Colors.BG)


@dataclass
class StyleSpec:
    color: ColorPairs


def wrapper(fxn: 'Composable', framerate: float = 60) -> Any:
    """This function is a wrapper around curses.wrapper which starts the extra
    features available in this framework. Ensure you use this function instead
    of curses.wrapper.
    """
    # Initialize the curses-related settings.
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)
    curses.start_color()
    stdscr.timeout(int(1000 / 60))

    try:
        # Initialize the compots framework settings.
        Colors.init_curses()
        ColorPairs.init_curses()

        ret = fxn(stdscr)
    finally:
        # Deconstruct everything
        curses.curs_set(1)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    return ret


class CompotProgram:
    def __enter__(self) -> 'CompotProgram':
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        self.stdscr.timeout(int(1000 / 60))
        Colors.init_curses()
        ColorPairs.init_curses()
        return self

    def __exit__(self, err_type, err_class, err_obj):
        curses.curs_set(1)
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
