# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:26:48 2021
Example creation/usage of context manager statements.

Notes from:
https://realpython.com/python-with-statement/#coding-class-based-context-managers
@author: Joe Raso
"""

# A context manager is used to create a block of code where
# - (a) certain actions always happen at the start
# - (b) cartain actions always happen at the close
# - (c) any exceptions raised only come up after the entire block is done.

class myContext:
    def __init__(self, name):
        self.name = name
    # Any context manager needs an enter
    def __enter__(self):
        print("Hello, {name}. We are now entering your context.")
    # ... and an exit (which takes the type, value anf throwback of any
    # exceptions that may have occured.
    def __exit__(self, etype, evalue, throwback):
        print("We are now leaving your context, with exception info:")
        print(etype, evalue, throwback, sep="\n")
        
# example usage:
with myContext('Joe') as hello:
    print("We are now inside the context")
    raise Exception()
    
# Context management are the ideal way to deal with file opening/closing
# files, accessing shared libraries, accessing certain APIs among many
# other applications.