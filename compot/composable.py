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

class ComposableMemos:
    """This class holds memoized Composables. The goal of this class is to
    provide a seamless interface.

    Todo:
        Realistically the implementation of this class is a good bit dumb (and
        I'm being really polite to myself here).

        There are two ways to envision memoization in compot that I currently
        see. One way is to do this in ``ComposableGraph``, however, that would
        require the graph to be a bit rewritten and, more importantly, would
        mean that each ``ComposableCursed`` would also have to be rewritten to
        facilitate the graph conditionally rebuilding children only if they
        aren't memoized. The problem with this is that currently all
        ``ComposableCursed`` objects actually call the ``build`` method of a
        ``ComposableT`` meaning that some changes to all widgets would be
        necessary.

        The other way is to keep an implementation that tracks each memoized
        type say (Text) and memoizes new instances unconditionally, keeping it
        in a CircularArray. The neat thing about this is that we end up caching
        not only Texts that have the same args and kwargs, but also their
        previous instances which could be very useful if a Text morphs from one
        state into another repeatedly. Imagine something like:

        .. code-block:: python

           @Composable
           def BlinkingText(state):
                if state.is_blinked:
                    return Text(state.text.is_on_text)
                else:
                    return Text(state.text.is_off_text)

        In this somewhat forced example you can see that it would be very
        useful for the Text to keep its previous state. I presume caching
        values like this would become very useful for when elements repeat
        their state (any sort of animation).
    """
    ACCESS_COUNT_THRESHOLD = 100

    def __init__(self) -> None:
        self._access_count = 0
        self._dict: Dict[int, Any] = {}

    def get_memo(self, c_name, c_args, c_kwargs) -> Any:
        self._access_count += 1
        if self._access_count > self.__class__.ACCESS_COUNT_THRESHOLD:
            self.clear()

        return self._dict.get(self.c_hash(c_name, c_args, c_kwargs))

    def c_hash(self, c_name, c_args, c_kwargs):
        return hash((c_name, c_args, frozenset(c_kwargs)))

    def put_memo(self, c_name, c_args, c_kwargs, memo) -> None:
        self._dict[self.c_hash(c_name, c_args, c_kwargs)] = memo

    def clear(self):
        self._dict.clear()
        self._access_count = 0

COMPOSABLE_MEMOS = ComposableMemos()


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


def ComposableCursed(
    measurement_strategy: Callable,
    memo: bool = False
) -> Callable:
    """A ``ComposableCursed`` is a lower-level mechanism for creating very
    fundamental ``ComposableT`` objects. This decorator allows for creating
    objects from low-level ``curses`` APIs.

    Please consult the documentation for more information.

    Parameters:
        measurement_strategy: The function used to measure the composable.
        memo (bool): A flag indicating whether this object should be memoized.
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
                new_args = args

                built = composable(*new_args, **new_kwargs)
                return built

            composable_t = ComposableT(
                name=composable.__name__,
                args=args,
                kwargs=kwargs,
                measurement_strategy=measurement_strategy,
                build=build_composable,
            )
            return composable_t

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
