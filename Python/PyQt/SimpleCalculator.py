# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:44:29 2021

A little calculator program, to test out QGridLayout, QLineEdit, and to
 experiment with wrapping widgets in a class structure

@author: Joe Raso
"""

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QGridLayout, QLineEdit, QVBoxLayout
    
app = QApplication([])

class SimpleCalculator:
    """A simple calculator widget function/object."""
    def __init__(self): 
        # Generate the input line, and set it up to be watched
        self.inputline = QLineEdit()
        self.curr_input = ''
        self.inputline.setText(self.curr_input)
        
        # Also set it to evaluate when 'enter' is pressed from the box
        self.inputline.returnPressed.connect(self.evaluate)
        
        # Set a grid for numerical buttons
        self.numpad = self.create_numpad()
        
    def inputbutton(self, inp):
        """Generates button objects that push whatever is on their label to
        the input field."""
        # Create the function for the button to add it's label to the input
        def pushed():
            self.curr_input = self.inputline.text()
            self.curr_input += str(inp)
            self.inputline.setText(self.curr_input)
            
        # create the button itself
        button = QPushButton(f"{inp}")
        button.clicked.connect(pushed)
        return button
        
    def evaluate(self):
        """The function that evaluates the current input field."""
        self.curr_input = self.inputline.text()
        ans = eval(self.curr_input)
        self.curr_input = str(ans)
        self.inputline.setText(self.curr_input)
        
    def create_numpad(self):
        """Function that generates the grid of input butttons."""
        # Set a grid for numerical buttons. It automatically tracks columns
        # and rows, without the need to pre-specify the dimensions.
        buttongrid = QGridLayout()
        
        # Add the numbered buttons
        n = 1
        for i in range(3):
            for j in range(3):
                buttongrid.addWidget(self.inputbutton(n),i,j)
                n += 1
                
        # Add 0 at the bottom, and '.'
        buttongrid.addWidget(self.inputbutton(0),3,1)
        buttongrid.addWidget(self.inputbutton("."),3,2)
        
        # Add the operations on the side
        buttongrid.addWidget(self.inputbutton("+"),0,3)
        buttongrid.addWidget(self.inputbutton("-"),1,3)
        buttongrid.addWidget(self.inputbutton("/"),2,3)
        buttongrid.addWidget(self.inputbutton("*"),3,3)
        
        # Create the evaluate button, and add it to the grid
        equals = QPushButton("=")
        equals.clicked.connect(self.evaluate)
        buttongrid.addWidget(equals,3,0)
        
        # Wrap in a widget
        numpad = QWidget()
        numpad.setLayout(buttongrid)
        return numpad
        
    def show(self):
        """Function that assembles and shows the app window."""
        # Set window up
        layout = QVBoxLayout()
        layout.addWidget(self.inputline)
        layout.addWidget(self.numpad)
        window = QWidget()
        window.setLayout(layout)
        
        # Exicute the window
        window.show()
        app.exec()

if __name__ == '__main__':
    
    calc = SimpleCalculator()
    calc.show()

