#!/usr/bin/env python

import _curses

from compot import MeasurementSpec, wrapper
from compot.widgets import StatusBar, Text


def __demo(stdscr: '_curses._CursesWindow') -> int:
    stdscr.clear()
    stdscr.refresh()

    bar_w = stdscr.getmaxyx()[1]

    StatusBar(
        (
            Text('Left Status'),
            Text('Center Status'),
            Text('Right Status')
        ),
        measurement=MeasurementSpec.xywh(0, 0, bar_w, 1)
    ).build().render()

    stdscr.getkey()

    return 0

if __name__ == '__main__':
    exit(wrapper(__demo))
