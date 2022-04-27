#!/usr/bin/env python

import curses
from dataclasses import dataclass
from enum import IntEnum
from functools import reduce
import operator
from typing import Tuple

from compot import LayoutSpec, MeasurementSpec, ColorPairs
from compot.composable import ComposableGraph, Measurement, ComposableCursed
from wcwidth import wcswidth

class _TextAlignment(IntEnum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


@dataclass
class _TextStyleSpec:
    color: ColorPairs = ColorPairs.INFO
    align: '_TextAlignment' = _TextAlignment.LEFT
    bold: bool = False
    italic: bool = False
    underline: bool = False

    def __repr__(self) -> str:
        return \
            '<' + ', '.join(x for x in (
                f'color={self.color.name}',
                f'align={self.align.name}',
                ('bold' if self.bold else ''),
                ('italic' if self.italic else ''),
                ('underline' if self.underline else ''),
            ) if x != '') + '>'

    def attrib_to_int(self, attrib: str) -> int:
        ATTRIB_MAP = {
            'color': lambda c: ColorPairs.get(c),
            'bold': lambda b: curses.A_BOLD if b else 0,
            'italic': lambda i: curses.A_ITALIC if i else 0,
            'underline': lambda u: curses.A_UNDERLINE if u else 0
        }

        return ATTRIB_MAP[attrib](getattr(self, attrib))

    def get_curses_of_attribs(self, attribs: Tuple[str, ...]) -> int:
        """Returns the resulting curses bitmask from the selected
        attribs. The attribs field is a tuple of strings targeting the
        selected fields."""
        return reduce(
            operator.or_,
            (self.attrib_to_int(a) for a in attribs),
            0
        )

    @property
    def curses(self) -> int:
        return self.get_curses_of_attribs((
            'color', 'bold', 'italic', 'underline'))

def __text_measurement_strategy(
    text: str,
    offered: Measurement = Measurement.inf(),
    layout: LayoutSpec = LayoutSpec.FIT_CONTENT,
    **kwargs
):
    if offered.h < 1:
        raise ValueError('Text requires at least 1 character of height.')

    if layout == LayoutSpec.FIT_CONTENT:
        return Measurement(min(offered.w, wcswidth(text)), 1)
    if layout == LayoutSpec.FILL:
        return offered

    return Measurement(offered.w, 1)

@ComposableCursed(__text_measurement_strategy)
def _Text(
    text: str,
    measurement: MeasurementSpec = MeasurementSpec.INJECTED(),
    layout: LayoutSpec = LayoutSpec.FIT_CONTENT,
    style: '_TextStyleSpec' = _TextStyleSpec(),
):
    ms = measurement

    window = curses.newwin(
        *MeasurementSpec.xywh(ms.x, ms.y, ms.w + 1, 1))

    # Now we need to do the left and right character padding
    renderable = text
    pad_count = (ms.w - wcswidth(text))

    if style.align == _TextAlignment.RIGHT:
        renderable = ' ' * pad_count + renderable
    if style.align == _TextAlignment.CENTER:
        pad_c_r = pad_count // 2
        pad_c_l = pad_c_r if pad_count % 2 == 0 else pad_c_r + 1
        renderable = pad_c_l * ' ' + text + pad_c_r * ' '
    if style.align == _TextAlignment.LEFT:
        renderable += ' ' * pad_count

    window.addnstr(renderable, ms.w, style.curses)

    return ComposableGraph(window)
