# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 12:10:46 2021
Sample creation/usage of decorators, with an examples: basic sample, timer and
call log decorators.
@author: Joe Raso
"""

import datetime
import functools

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
def myTimer(func):
    """Decorator that prints the timestamp when the function call complete
    displaying the time elapsed during the function call."""
    # functools.wraps decorator makes a wrapping function give the call 
    # signature of the function it wraps, making it easier to trace a function
    # when it could have multiple decorators:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tic = datetime.datetime.now()
        out = func(*args, **kwargs)
        toc = datetime.datetime.now()
        elapsed = int((toc-tic).total_seconds())
        print(f"{toc.time()}: Function '{func.__name__}' finished in "+\
            "{elapsed} sec.")
        return out
    # Note that for more detailed log information, try using func.__str__()
    # which includes things like the memory address of the function.
    return wrapper
    
def myLog(func):
    """Decorator that prints the timestamp when the function is called, 
    diplaying it's input args and kwargs."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tic = datetime.datetime.now()
        print(f"{tic.time()}: Called {func.__name__}{args}, kwargs={kwargs}.")
        return func(*args, **kwargs)
    return wrapper
    
if __name__ == '__main__':

    # functions are decorated by putting the '@decorator' statement directly
    # before the function definition.
    @sampleDecorator
    def example1():
        print("Hello")
    example1()

    print(50*'-')

    # Functions can have multiple decorators:
    @myTimer
    @myLog
    def example2(x, y, test=True):
        print(f"{x} + {y} = {x+y}")
        return x+y
    a = example2(3, 5, test=True)