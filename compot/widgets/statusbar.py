#!/usr/bin/env python

from typing import Tuple
from compot import LayoutSpec, MeasurementSpec
from compot.composable import ComposableT, Composable
from compot.widgets import Row, RowSpacing

@Composable
def _StatusBar(
    content: Tuple[Tuple[ComposableT, ...],
                   Tuple[ComposableT, ...],
                   Tuple[ComposableT, ...]],
    measurement: MeasurementSpec = MeasurementSpec.INJECTED()
):
    row = Row(
        children=content,
        measurement=measurement,
        layout=LayoutSpec.FILL,
        spacing=RowSpacing.SPACE_BETWEEN
    )
    return row
