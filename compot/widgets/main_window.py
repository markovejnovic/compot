#!/usr/bin/env python

from compot import CompotProgram, MeasurementSpec, wrapper
import reactivex as rx
import _curses

def _MainWindow(child, framerate=60) -> rx.Observable:
    """The ``MainWindow`` class returns a ``reactivex.Observable`` stream that
    you can hook into to register for inputs. To use this class successfully,
    you can look at the following example:

    Parameters:
        child (Composable): The child to attempt to render
        framerate (float): The target framerate. Keep it reasonable.

    .. code-block:: python

       my_composable = Column((Row(...), ...))
       input_obserable = MainWindow(my_composable)
       input_obserable.subscribe(on_next=lambda key: logging.info(key))

    """


    def _curses_function(stdscr: '_curses._CursesWindow'):
        height, width = stdscr.getmaxyx()
        child.build(
            measurement=MeasurementSpec.xywh(0, 0, width, height)).render()

        return stdscr.getch()

    def reactive_window(observer, scheduler):
        with CompotProgram() as prog:
            try:
                while True:
                    if (key := _curses_function(prog.stdscr)) != -1:
                        observer.on_next(chr(key))
            except Exception as ex:
                observer.on_error(ex)
            finally:
                observer.on_completed()

    return rx.create(reactive_window)
