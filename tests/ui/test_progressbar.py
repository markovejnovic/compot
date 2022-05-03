#!/usr/bin/env python

import _curses

import time
from compot import LayoutSpec, MeasurementSpec, wrapper
from compot.widgets import ProgressBar, Text, Row


def __demo(stdscr: '_curses._CursesWindow') -> int:
    bar_w = stdscr.getmaxyx()[1]

    TARGET_FPS = 144
    start = time.time()
    last = time.time()
    while (current := time.time()) - start < 10:
        # Fps throttler
        render_time = current - last
        time.sleep(max(1 / TARGET_FPS - render_time, 0))
        last = current

        total_time = current - start

        stdscr.erase()
        ProgressBar(
            total_time / 10,
            measurement=MeasurementSpec.xywh(0, 0, bar_w, 1)
        ).build().render()

        Row((ProgressBar(total_time / 10), ),
            measurement=MeasurementSpec.xywh(0, 11, bar_w, 1),
            layout=LayoutSpec.FILL
        ).build().render()

        Text(
            f'FPS: {round(1 / render_time)}',
            measurement=MeasurementSpec.xywh(0, 10, bar_w, 1)
        ).build().render()

    stdscr.getch()

    return 0

if __name__ == '__main__':
    exit(wrapper(__demo))
