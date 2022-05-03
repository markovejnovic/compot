#!/usr/bin/env python

from typing import Iterable
from compot import LayoutSpec, Measurement, MeasurementSpec

from compot.composable import ComposableCursed, ComposableGraph, ComposableT


def __column_measurement_strategy(
    children: Iterable[ComposableT],
    offered: Measurement = Measurement.inf(),
    **kwargs
):
    if offered.h < 1:
        raise ValueError('A column requires 1 character of height.')

    return Measurement(
        offered.w,
        min(sum(c.measurement_strategy(*c.args, **c.kwargs).h \
                for c in children), offered.h),
    )

@ComposableCursed(measurement_strategy=__column_measurement_strategy)
def _Column(
    children: Iterable[ComposableT],
    measurement: MeasurementSpec = MeasurementSpec.INJECTED(),
):
    ms = measurement

    total_children_height = 0
    children_heights = []
    renderable_children = []
    for child in children:
        offered_h = ms.h - total_children_height
        if offered_h == 0:
            break

        child_height = child.measurement_strategy(
            *child.args,
            offered=Measurement(ms.w, ms.h - total_children_height),
            **child.kwargs
        ).h
        children_heights.append(child_height)
        renderable_children.append(child)
        total_children_height += child_height

    children_windows = []
    y_pos = 0
    for child, child_height in zip(renderable_children, children_heights):
        child_window = child.build(
            measurement=MeasurementSpec.xywh(
                ms.x,
                ms.y + y_pos,
                ms.w,
                child_height
            )
        )
        y_pos += child_height
        children_windows.append(child_window)

    return ComposableGraph(None, children_windows)

