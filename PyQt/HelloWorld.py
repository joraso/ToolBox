# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 09:17:43 2021

Experimenting with creating GUI elements with PyQt, starting with a simple
"Hello World" popup.

Notes copied from:
https://build-system.fman.io/pyqt5-tutorial

@author: Joe Raso
"""

from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication([])
# This is a requirement of Qt: Every GUI app must have exactly one instance
# of QApplication. Many parts of Qt don't work until you have executed the
# above line. You will therefore need it in virtually every (Py)Qt app you
# write. The brackets [] in the above line represent the command line
# arguments passed to the application. Because our app doesn't use any
# parameters, we leave the brackets empty.

# Define a simple label window
label = QLabel('Hello World!')
label.show()

# The last step is to hand control over to Qt and ask it to "run the
# application until the user closes it". This is done via the command:
app.exec()
