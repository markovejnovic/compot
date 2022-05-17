#!/usr/bin/env python

from compot.widgets import MainWindow, Column, Row, Text, RowSpacing


def demo():
    inputs = MainWindow(
        Column(
            (
                Row((Text('Hello World--'), Text('=>Once more in the row'))),
                Text('Bye Cruel World')
            )
        )
    )
    def what_do(i):
        pass

    inputs.subscribe(on_next=what_do)

if __name__ == '__main__':
    demo()
