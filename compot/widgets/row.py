#!/usr/bin/env python

from enum import IntEnum

from typing import Iterable

from compot.composable import ComposableGraph, Measurement, ComposableCursed, \
    ComposableT
from compot import LayoutSpec, MeasurementSpec


class _RowSpacing(IntEnum):
    """The ``RowSpacing`` determines how a row should attempt to space
    children.

    If set to ``NONE`` then the children will have no spacing between them and
    will be placed all on the left of the row.
    If set to ``SPACE_BETWEEN`` then all the children will be placed in such a
    manner such that the space between them is maximized.

    An example diagram is:

    .. code-block:: text

       [(NONE)(NONE)(NONE)                               ]
       [(SPACE_BETWEEN)  (SPACE_BETWEEN)  (SPACE_BETWEEN)]

    """
    NONE = 0
    SPACE_BETWEEN = 1


def __row_measurement_strategy(
        children: Iterable[ComposableT],
        layout: LayoutSpec = LayoutSpec.FIT_CONTENT,
        offered: Measurement = Measurement.inf(),
        **kwargs
):
    if offered.h < 1:
        raise ValueError('Row requires 1 character of height.')

    if layout == LayoutSpec.FIT_CONTENT:
        return Measurement(
            min(sum(c.measurement_strategy(*c.args, **c.kwargs).w \
                    for c in children), offered.w), 1)
    if layout == LayoutSpec.FILL:
        return Measurement(offered.w, 1)

    return Measurement(offered.w, 1)

@ComposableCursed(measurement_strategy=__row_measurement_strategy)
def _Row(
    children: Iterable[ComposableT],
    measurement: MeasurementSpec = MeasurementSpec.INJECTED(),
    layout: LayoutSpec = LayoutSpec.FIT_CONTENT,
    spacing: _RowSpacing = _RowSpacing.NONE
):
    """A Row is a fundamental ``Composable`` widget that displays its elements
    in a single 1-character-high row.

    Parameters:
        children (Iterable[ComposableT]): The children to render.
        measurement (MeasurementSpec): The measurement specification the
            ``Row`` should adhere to. Usually, this is unnecessary as the
            parent will inject its ``MeasurementSpec`` into the ``Row``.
        layout (LayoutSpec): The layout specifications for the ``Row``. If set
            to ``LayoutSpec.FIT_CONTENT`` the row will force its width to be as
            wide as its content. If set to ``LayoutSpec.FILL`` then the ``Row``
            will adhere to whatever dimensions the parent requested.
        spacing (RowSpacing): The spacing strategy the ``Row`` should adhere
            to. This is only relevant if layout is set to ``LayoutSpec.FILL``.
    """
    ms = measurement

    # Let us first measure the children.
    total_children_width = 0
    children_widths = []
    child_count = 0
    for child in children:
        child_width = child.measurement_strategy(
            *child.args,
            offered=Measurement(ms.w - total_children_width, 1),
            **child.kwargs
        ).w
        children_widths.append(child_width)
        total_children_width += child_width
        child_count += 1

    padding = (ms.w - total_children_width) // (child_count - 1) \
        if spacing == _RowSpacing.SPACE_BETWEEN \
        else 0

    children_windows = []
    x_pos = 0
    for child, child_width in zip(children, children_widths):
        child_window = child.build(
            measurement=MeasurementSpec.xywh(
                ms.x + x_pos, measurement.y,
                child_width,
        1))

        x_pos += child_width + padding
        children_windows += [child_window]


    return ComposableGraph(None, children_windows)
