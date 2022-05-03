#!/usr/bin/env python

from dataclasses import dataclass, field
from math import floor
from typing import Dict
from compot import ColorPairs, LayoutSpec, MeasurementSpec
from compot.composable import Composable
from compot.widgets import Row, RowSpacing, Text, TextStyleSpec

BLOCK_MAP = {
    0/8: ' ',
    1/8: '▏',
    2/8: '▎',
    3/8: '▍',
    4/8: '▌',
    5/8: '▋',
    6/8: '▊',
    7/8: '▉',
    8/8: '█'
}

def _round_to_eighth(x: float) -> float:
    return round(x * 8) / 8

@dataclass
class _ProgressBarStyle:
    segments: Dict[float, Dict[str, ColorPairs]] = field(
        default_factory=lambda: {
            1/3: {'color': ColorPairs.ERROR},
            2/3: {'color': ColorPairs.WARNING},
            3/3: {'color': ColorPairs.OK}
        })

@Composable
def _ProgressBar(
    progress,
    *args,
    measurement: MeasurementSpec = MeasurementSpec.INJECTED(),
    style: _ProgressBarStyle = _ProgressBarStyle(),
    **kwargs
):
    avail_space = measurement.w - 2

    last_threshold = 0
    threshold_up = 0

    # Create a list of segments that are fully filled out.
    full_segments = []
    for threshold, s_style in style.segments.items():
        if progress < threshold:
            threshold_up = threshold
            break
        txt_size = int((threshold - last_threshold) * avail_space)
        full_segments.append(
            Text(BLOCK_MAP[1.0] * txt_size,
                 style=TextStyleSpec(color=s_style['color']))
        )
        last_threshold = threshold

    # Create a partial segment then.
    remaining_progress = (progress - last_threshold) * avail_space
    partial_size = int(floor(remaining_progress))
    rounded = _round_to_eighth(remaining_progress - partial_size)
    partial_segment = Text(
        BLOCK_MAP[1.0] * partial_size + BLOCK_MAP[rounded],
        style=TextStyleSpec(color=style.segments[threshold_up]['color'])
    )

    return Row(
        (
            Row((Text('['), Row(full_segments + [partial_segment]))),
            Row((Text(']'), ))
        ),
        *args,
        measurement=measurement,
        layout=LayoutSpec.FILL,
        spacing=RowSpacing.SPACE_BETWEEN,
        **kwargs,
    )
