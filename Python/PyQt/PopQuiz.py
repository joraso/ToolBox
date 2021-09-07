# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 17:47:43 2021

Walking through a rudimentry layout, buttons and signal/slot usage with PyQt5
by building a True/False popup quiz.

Created with help from:
https://build-system.fman.io/pyqt5-tutorial
https://build-system.fman.io/static/public/files/widgets_example.py

@author: Joe Raso
"""

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, \
    QVBoxLayout, QPushButton, QMessageBox

app = QApplication([])

def TrueFalseBox(question):
    """Little section of code that exicutes a True-False question box."""
    
    # Defining the layout layers and window
    window = QWidget()
    buttonbox = QWidget()
    innerlayout = QHBoxLayout()
    outerlayout = QVBoxLayout()

    # Define the buttons
    button1 = QPushButton("True")
    button2 = QPushButton("False")
    
    # create a function to exicute when a button is clicked
    ans = None
    def click_true():
        nonlocal ans
        ans = True
        window.close()
    def click_false():
        nonlocal ans
        ans = False
        window.close()
        
    # bind the function to the buttons
    button1.clicked.connect(click_true)
    button2.clicked.connect(click_false)
    
    # Setting the buttons next to each other in the buttonbox
    innerlayout.addWidget(button1)
    innerlayout.addWidget(button2)
    buttonbox.setLayout(innerlayout)
    
    # Stacking the buttons with the label in the outer layout
    label = QLabel(question)
    outerlayout.addWidget(label)
    outerlayout.addWidget(buttonbox)
    
    # Exicute the window
    window.setLayout(outerlayout)
    window.show()
    app.exec()
    return ans

def PopQuiz():
    """Uses the T/F box above to administer a quick little pop quiz."""
    
    # Set some questions and their answers in a dictionary
    questions = {"When water freezes, it's entropy increases.":False,
        "When water freezes, the entropy of the universe increases":True}
        
    # run through the questions and track how many are answered correctly        
    score = 0
    for q in questions.keys():
        ans = TrueFalseBox(q)
        score += int(ans == questions[q])

    # display the score at the end of the quiz
    result = QMessageBox()
    result.setText(f'You scored {score} correct')
    result.exec()
    
PopQuiz()