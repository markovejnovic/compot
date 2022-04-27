#!/usr/bin/env python

"""This module exposes the fundamental types that **compot** uses. These are
used to create widgets and compose widgets from other widgets."""

import _curses
from dataclasses import dataclass
from typing import Callable, Any, Dict, List, Optional, Tuple
from compot.datastructures import GeneralTree
from compot import MeasurementSpec, Measurement


@dataclass
class ComposableT:
    """A ComposableT is a data structure that holds all the information
    required to construct a ``ComposableGraph`` object. This ``dataclass``
    holds the name of the requested ``Composable``, the arguments that were
    passed, the measurement strategy and the ``build`` function (which is in
    reality the function that actually builds the ``ComposableGraph``.

    Due to how ``compot`` works, upon invoking a ``Composable`` function, this
    object is returned rather than the graph itself. In other words:

    .. code-block:: python

       @Composable
       def MyComposable(...):
           ...

       my_composable = MyComposable()
       type(my_composable) == 'ComposableT'

       # The graph can be accessed with
       my_composable.build()
    """
    name: str
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    measurement_strategy: Callable[[Any], Measurement]
    build: Callable[[], 'ComposableGraph']

    def __repr__(self) -> str:
        args = ', '.join(repr(a) for a in ar) \
            if len((ar := self.args)) > 0 \
            else ''
        kwargs = ', '.join(f'{k}={repr(a)}' for k, a in kw.items()) \
            if len((kw := self.kwargs)) > 0 \
            else ''
        return f'{self.name}<{args}{", " if kwargs and args else ""}{kwargs}>'

ComposableF = Callable
MeasurementStrat = Callable
ComposableCallable = Callable

ComposableFunction = Callable[[Any, Any], ComposableT]

def Composable(composable: ComposableFunction) -> Callable:
    """A Composable is a UI element that can be composed with other elements.
    This is a 1-to-0.5 conversion of the Android ``jetpack-compose`` library
    without all the effort.

    This function has been designed to be used as a decorator enabling you to
    create your own TUI elements that you can then compose together.

    To exemplify:

    .. code-block:: python

       @Composable
       def StatusBar(content, *args, **kwargs):
           return Row(
               (Row(c) for c in content),
               *args, **kwargs
           )

    This code example wraps the ``Row`` elements that are built from your
    ``content`` in another ``Row``, such that the outer ``Row`` spaces between
    the elements as much as it can.
    """
    def wrapper(*args: Any, **kwargs: Any) -> ComposableT:
        return composable(*args, **kwargs)
    return wrapper


def ComposableCursed(measurement_strategy: Callable) -> Callable:
    """A ``ComposableCursed`` is a lower-level mechanism for creating very
    fundamental ``ComposableT`` objects. This decorator allows for creating
    objects from low-level ``curses`` APIs.

    Please consult the documentation for more information.
    """
    def factory(composable: ComposableF) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> ComposableT:
            def build_composable(*cargs: Any, **ckwargs):
                pushed_args = args + cargs
                pushed_kwargs = {**kwargs, **ckwargs}
                try:
                    old_measurements = pushed_kwargs['measurement']
                except KeyError as k_err:
                    raise ValueError(
                        f'{composable.__name__} was called without a '
                        'measurement. This likely means you are using a '
                        'top-level widget without specifying its '
                        'measurements.') from k_err
                measurements = measurement_strategy(
                    *pushed_args, offered=old_measurements, **pushed_kwargs)
                new_kwargs = {
                    **pushed_kwargs,
                    'measurement': MeasurementSpec.xywh(
                        old_measurements.x,
                        old_measurements.y,
                        measurements.w,
                        measurements.h
                    )
                }
                return composable(*args, **new_kwargs)

            return ComposableT(
                name=composable.__name__,
                args=args,
                kwargs=kwargs,
                measurement_strategy=measurement_strategy,
                build=build_composable
            )
        return wrapper
    return factory


class ComposableGraph:
    """Represents a graph that holds all the curses windows to be rendered."""
    def __init__(self,
                 me: Optional['_curses._CursesWindow'],
                 children: List['ComposableGraph'] = []) -> None:
        # Man generics suck in python
        self.__ds_tree = GeneralTree['_curses._CursesWindow'](me, children)

    def __str__(self) -> str:
        return (f'ComposableGraph<node={self.__ds_tree.node}, '
                f'children={self.apply(lambda t: str(t))}>')

    def apply(self, predicate):
        return self.__ds_tree.apply(predicate)

    def render(self):
        def _render_tree(window):
            if window:
                window.refresh()
        self.__ds_tree.apply(_render_tree)
