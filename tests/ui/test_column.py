#!/usr/bin/env python

#!/usr/bin/env python

import _curses
from compot import LayoutSpec, MeasurementSpec, ColorPairs, wrapper
from compot.widgets import Text, TextStyleSpec, Row, RowSpacing, Column


def __demo(stdscr: '_curses._CursesWindow') -> int:
    stdscr.clear()
    stdscr.refresh()

    Column(
        (
            Text('Hello'),
            Text('World'),
            Text('In'),
            Text('Column')
        ),
        measurement=MeasurementSpec.xywh(0, 0, 100, 4)
    ).build().render()

    Column(
        (
            Text('Hello'),
            Text('World'),
            Text('In'),
            Text('Column'),
            Text('Too Big...'),
            Text('I\'m not there')
        ),
        measurement=MeasurementSpec.xywh(0, 4, 100, 5)
    ).build().render()

    Column(
        (
            Row(
                (
                    Text('Now I am In a Row--'),
                    Text('==>Same Row')
                )
            ),
            Row(
                (
                    Text('Now I am In another Row--'),
                    Text('==>Same Row')
                )
            ),
            Text('Yet we (and me is a Text) live in the same column'),
        ),
        measurement=MeasurementSpec.xywh(0, 9, 100, 3)
    ).build().render()

    stdscr.getkey()

    return 0

if __name__ == '__main__':
    exit(wrapper(__demo))
