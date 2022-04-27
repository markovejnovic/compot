#!/usr/bin/env python

import _curses
from compot import LayoutSpec, MeasurementSpec, ColorPairs, wrapper
from compot.widgets import Text, TextStyleSpec, Row, RowSpacing


def __demo(stdscr: '_curses._CursesWindow') -> int:
    stdscr.clear()
    stdscr.refresh()

    bar_w = stdscr.getmaxyx()[1]

    Row(
        (
            Text(text='Hello '),
            Text(text='World')
        ),
        measurement=MeasurementSpec.xywh(0, 0, bar_w, 1)
    ).build().render()

    Row(
        (
            Text(
                text='Shift >>> Hello RED ',
                style=TextStyleSpec(
                    color=ColorPairs.ERROR_INVERTED
                )
            ),
            Text(
                text=' Goodbye Green bold',
                style=TextStyleSpec(
                    color=ColorPairs.OK_INVERTED,
                    bold=True
                )
            )
        ),
        measurement=MeasurementSpec.xywh(10, 1, bar_w - 10, 1)
    ).build().render()

    Row(
        (
            Row(
                (
                    Text(
                        text='I\'m in a subrow',
                        style=TextStyleSpec(
                            color=ColorPairs.ERROR_INVERTED
                        )
                    ),
                    Text(
                        text=' So am I',
                        style=TextStyleSpec(
                            color=ColorPairs.OK_INVERTED,
                            bold=True
                        )
                    )
                )
            ),
            Text(
                text=' Goodbye Yellow bold, but this is very long',
                style=TextStyleSpec(
                    color=ColorPairs.WARNING_INVERTED,
                    bold=True
                )
            )
        ),
        measurement=MeasurementSpec.xywh(4, 2, bar_w, 1)
    ).build().render()

    Row(
        (Text('I am a row that got filled with a child way too big.'),),
        measurement=MeasurementSpec.xywh(0, 3, 50, 1),
    ).build().render()

    Row(
        (
            Text('I am on the left'),
            Text('And I am on the very right')
        ),
        measurement=MeasurementSpec.xywh(0, 4, bar_w, 1),
        layout=LayoutSpec.FILL,
        spacing=RowSpacing.SPACE_BETWEEN
    ).build().render()

    stdscr.getkey()

    return 0

if __name__ == '__main__':
    exit(wrapper(__demo))
