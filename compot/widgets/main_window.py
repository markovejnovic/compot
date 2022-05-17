#!/usr/bin/env python

from compot import CompotProgram, MeasurementSpec, wrapper
import reactivex as rx
import reactivex.operators as rxops
import _curses

from compot.composable import ComposableT

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


def _ObserverMainWindow(child, data: rx.Observable):
    """The ``ObserverMainWindow`` subscribes to data and renders its children
    based on data changes.

    Example:

    .. code-block:: python

       ObserverMainWindow(MyCustomWidget, my_data_to_subscribe_to)

    Note:
        The ``CompotProgram`` will not be closed until you call
        ``on_completed`` on the observable. This means that if you abruptly
        exit the program, your terminal **will be ruined**. Make sure you call
        ``on_completed``.

    Todo:
        Support key events.
    """
    prog = CompotProgram()

    def rerender_window(state):
        max_h, max_w = prog.stdscr.getmaxyx()

        try:
            child(
                state,
                measurement=MeasurementSpec.xywh(0, 0, max_w, max_h)
            ).build().render()
            prog.stdscr.getch()
        except Exception as err:
            prog.close()
            raise err

    def close():
        prog.close()

    def on_err(error):
        prog.close()

    data.pipe(rxops.sample(1 / 60)).subscribe(
        rerender_window, on_err, close)
