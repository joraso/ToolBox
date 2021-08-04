# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 14:10:55 2021
Practive implementing / example of python objects with built-in methods.

Built in methods interact with the interpreter, and can be used to overload
it's built in functionality as shown below.

This allows you to create object that, for example, have defined behavior
under +, -, *, or a predetermined way they print!
@author: Joe Raso
"""

import math

class Complex(object):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    def __add__(self, no):
        return Complex(self.real+no.real, self.imaginary+no.imaginary)
    def __sub__(self, no):
        return Complex(self.real-no.real, self.imaginary-no.imaginary)
    def __mul__(self, no):
        return Complex(self.real*no.real - self.imaginary*no.imaginary,
                      + self.real*no.imaginary + self.imaginary*no.real)
    def __truediv__(self, no):
        no_conj = Complex(no.real, -no.imaginary)
        noabs2 = no.real**2 + no.imaginary**2
        return Complex((self * no_conj).real / noabs2,
                       (self * no_conj).imaginary / noabs2)
    def mod(self):
        """the modulus, a.k.a. absolute value."""
        return math.sqrt(self.real**2 + self.imaginary**2)
    def __str__(self):
        # this snippet is from the authors at Hacker Rank
        if self.imaginary == 0:
            result = "%.2f+0.00i" % (self.real)
        elif self.real == 0:
            if self.imaginary >= 0:
                result = "0.00+%.2fi" % (self.imaginary)
            else:
                result = "0.00-%.2fi" % (abs(self.imaginary))
        elif self.imaginary > 0:
            result = "%.2f+%.2fi" % (self.real, self.imaginary)
        else:
            result = "%.2f-%.2fi" % (self.real, abs(self.imaginary))
        return result
        
if __name__ == '__main__':
    c = Complex(1, 2)
    d = Complex(3, 2)
    print(c)
    print(d)
    print(c/d)
    
    print(c.mod())
    
    # using the built in class
    c = complex(1, 2)
    d = complex(3, 2)
    print(c)
    print(d)
    print(c/d)
#    x = Complex(*c)
#    y = Complex(*d)
#    print(*map(str, [x+y, x-y, x*y, x/y, x.mod(), y.mod()]), sep='\n')