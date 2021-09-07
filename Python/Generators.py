# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:59:46 2021
Basic creation/usage of a generator, with Fibonacci number example.
@author: Joe Raso
"""

from sys import getsizeof

def Fibonacci(n):
    """Generator for the first n Fibonacci numbers."""
    f1 = 0; f2 = 1
    for i in range(n): # note that range() iteslf is NOT a generator.
        # Here is where the magic happens: 'yield' pauses the function and
        # returns value. When the next value is requested (with 'next()' or
        # in anything that iterates, like a for loop), it continues until it
        # finds the next yield statement. Yielding instead of returning is the
        # halmark that the function is a generator.
        yield f1
        # apply the Fibonacci rule to get the next number
        f1, f2 = f2, f1 + f2
        
if __name__ == '__main__':
    
    # Generator are useful for looping:
    print ("Looping over the first 10 fibonacci numbers:")
    for f in Fibonacci(10):
        print(f)
        
    print(50*'-')
    
    # Or values gan be retrieved with next
    print("Calling Fibonacci numbers with 'next()':")
    fib = Fibonacci(10)
    print(next(fib), end=', ')
    print(next(fib), end=', ')
    print(next(fib))
    
    print(50*'-')
    
    # But they don't store their values, making them very memory efficient:
    print("Comparing a generator and list size for 1000 Fibonacci numbers:")
    fgen = Fibonacci(1000)
    print(f"The generator takes up {getsizeof(fgen)} bytes,", end=' ')
    flist = list(fgen)
    print(f"while the list takes up {getsizeof(flist)} bytes.")
    
    print(50*'-')
    
    # They can also be constructed in a manner similar to list comprehension
    # by simply replacing the "[]" with "()".
    print("Creating generators on the fly:")
    Squares10a = [x**2 for x in range(10)] 
    print(f"Squares10a is {Squares10a.__str__()}") # this is a list
    Squares10b = (x**2 for x in range(10))
    print(f"Squares10b is {Squares10b.__str__()}") # this is a generator
    
    print(50*'-')
    
    # To investigate later: .send(), .throw(), .close()