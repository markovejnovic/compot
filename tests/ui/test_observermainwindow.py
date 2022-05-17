#!/usr/bin/env python

import time
import threading
import reactivex as rx
import reactivex.operators as rxops
from dataclasses import dataclass
from compot import MeasurementSpec
from compot.widgets import ObserverMainWindow, Column, Row, Text
from compot.composable import Composable

@dataclass
class CustomModel:
    a: str
    b: str
    c: str


@Composable
def test_view(model: CustomModel, measurement = MeasurementSpec.INJECTED()):
    return Column((
        Row((Text(model.a), Text(model.b))),
        Text(model.c)
    ), measurement=measurement)

def demo():
    subject = rx.Subject()
    def feed_subject(subject: rx.Subject):
        for i in range(1000):
            subject.on_next(CustomModel('Hello ', 'World', f'{i}'))
            time.sleep(1e-2)

    try:
        provider_thread = threading.Thread(target=feed_subject, args=(subject, ))
        window = ObserverMainWindow(test_view, subject)
        provider_thread.start()

        provider_thread.join()

        subject.on_completed()
    except KeyboardInterrupt as key_int:
        subject.on_error(key_int)

if __name__ == '__main__':
    demo()
