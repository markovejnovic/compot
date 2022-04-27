# compot

Compot is a simple, compositional framework for building TUIs. It is heavily
inspired by `jetpack-compose` and strives to be its equivalent in TUIs.

Currently, it is in its early stages of development as I do not have much time
to dedicate it and am developing it for internal use at work. As requirements
expand, so too will `compot`.

## Features

* Abstractions beyond low-level `curses`
* Fully Stateless
* Lazy Rendering
* Fully written in python

What all this means is that `curses` development becomes a breeze. Here's an
example:
```python

@Composable
def StatusBar(
    content: Tuple[Tuple[ComposableT, ...],
                   Tuple[ComposableT, ...],
                   Tuple[ComposableT, ...]],
    measurement: MeasurementSpec = MeasurementSpec.INJECTED()
):
    return Row(
        children=content,
        measurement=measurement,
        layout=LayoutSpec.FILL,
        spacing=RowSpacing.SPACE_BETWEEN
    )
```

This is the source code for the `StatusBar` widget. To invoke it, run it with:

```python

StatusBar(
    (
        Text('Left Status'),
        Text('Center Status'),
        Text('Right Status')
    ),
    measurement=MeasurementSpec.xywh(0, 0, bar_w, 1)
).build().render()
```

Only the top level element needs to know its measurements (as of now, there is
no `MainWindow`-like widget that would handle this for you automatically), and
everything else gathers its measurements automatically

Note some of the cool things here:

* Until you call `Composable.build()` nothing actually gets invoked. Simply
    calling `StatusBar` just makes a very small data structure that holds all
    the data required to build the `StatusBar`, but until you call `build` its
    measurements, its specs are all indeterminate. Calling `build` then forces
    the UI element to actually figure out its dimensions and create all the
    required objects. Usually this requires the widget to ask its child widgets
    to predict how large they are going to be, but even then, only the bare
    minimum is done to actually measure the widgets. `build` then constructs a
    graph that is rendered with `render()`.
* Everything is automatic! Where do I position the `Left Status` text? Where
    does `Center Status` go? What about `Right Status`? **We don't care.**
    `StatusBar` figures it out (actually, the
    `spacing=RowSpacing.SPACE_BETWEEN`) value given to `Row` in `StatusBar`
    forces the desired `StatusBar` behavior.

## The downsides

* The codebase is in a state of improvement and development.
* The API is bound to change.
* The number of widgets is too small to make a usable product out of this as of
    now.

## Requirements

The only requirement is that you have `python > 3.8`. I do not plan to support
lower versions of `python` and cannot help in supporting them.

## Installing

You should be able to get up and running by running

```bash
pip install compot-ui
```

## Tests

Tests are very rudimentary and you must manually test all the widgets that are
available currently. Check the `tests/ui` directory and run each of the scripts
to see how they appear.

## Licensing

```text
Copyright 2022 Marko Vejnovic

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
