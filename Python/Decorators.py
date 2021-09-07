# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 12:10:46 2021

Sample usage of decorators, with an example timer/log decorator.

@author: Joe Raso
"""

import datetime

# Decorator functions return wrappers on another function:
def sampleDecorator(func):
    # Use *args and **kwargs so that the wrapper takes the same input as the
    # wrapped function.
    def wrapper(*args, **kwargs):
        print("this function...")
        out = func(*args, **kwargs)
        print("has been wrapped.")
        # remember to return the output of the wrapped function so that
        # it's usage in the program won't be disrupted. Unless that's what you
        # want, I guess.
        return out
    return wrapper
    
# Useful for things like timers and/or debugging logs:
def myTimerLog(func):
    """Wrapper that prints log entries to std: first when the function is
    called, diplaying it's input, and second when the function call complete
    displaying the time elapsed."""
    def wrapper(*args, **kwargs):
        tic = datetime.datetime.now()
        print(f"{tic.time()}: Called {func.__name__}{args}, kwargs={kwargs}.")
        out = func(*args, **kwargs)
        toc = datetime.datetime.now()
        elapsed = int((toc-tic).total_seconds())
        print(f"{toc.time()}: Function '{func.__name__}' finished in "+\
            "{elapsed} sec.")
        return out
    # Note that for more detailed log information, try using func.__str__()
    # which includes things like the memory address of the function.
    return wrapper
    
if __name__ == '__main__':

#    @sampleDecorator
    @myTimerLog
    def example(x, y, test=True):
        print(f"{x} + {y} = {x+y}")
        return x+y
        
    a = example(3, 5, test=True)