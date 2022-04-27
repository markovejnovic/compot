#!/usr/bin/env python

import _curses
from compot import MeasurementSpec, ColorPairs, LayoutSpec, wrapper
from compot.widgets import Text, TextStyleSpec, TextAlignment

def __demo(stdscr: '_curses._CursesWindow') -> int:
    stdscr.clear()
    stdscr.refresh()

    bar_w = stdscr.getmaxyx()[1]

    Text(
        'Hello World',
        measurement=MeasurementSpec.xywh(0, 0, bar_w, 1)
    ).build().render()

    text_composable = Text('Hello World but on another line',
         measurement=MeasurementSpec.xywh(0, 1, bar_w, 1))
    text_composable.build().render()

    text_composable = Text('Hello World but on another line AND shifted',
         measurement=MeasurementSpec.xywh(50, 2, bar_w, 1))
    text_composable.build().render()

    text_composable = Text('Hello World but on another line AND shifted',
         measurement=MeasurementSpec.xywh(50, 2, bar_w, 1))
    text_composable.build().render()

    text_composable = Text(
        text='Hello World (style+shift)',
        measurement=MeasurementSpec.xywh(30, 3, bar_w, 1),
        style=TextStyleSpec(
            color=ColorPairs.WARNING_INVERTED,
            bold=True
        )
    )
    text_composable.build().render()

    Text(
        text='Hello World (fill+underline)',
        measurement=MeasurementSpec.xywh(0, 4, bar_w, 1),
        layout=LayoutSpec.FILL,
        style=TextStyleSpec(
            color=ColorPairs.ERROR_INVERTED,
            align=TextAlignment.CENTER,
            underline=True,
        )
    ).build().render()

    Text(
        'I am way too big for my own good.',
        measurement=MeasurementSpec.xywh(0, 5, 31, 1)
    ).build().render()

    stdscr.getkey()

    return 0

if __name__ == '__main__':
    exit(wrapper(__demo))
