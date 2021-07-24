# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 19:49:41 2021
Sorting algorithms
@author: promethustra
"""

def QuickSort(a, i=None, j=None):
    """Implementation of the quicksort algorithm for a python list of integers,
    sorting in ascending value. Runs at O(n^2) in the worst case, and 
    O(n*log2(n)) in the best case."""
    # Null / short list escape
    if len(a) < 2:
        return a                     
    # set counters to initial positions
    i = 0; j = len(a)-1    
    # pick the pivot as 1/2-way
    pivot = a[int(len(a)/2)]         
#    print(a,', pivot=', pivot)
    # scroll through to find values to that need to be swapped
    while i < j: 
#        print("i=",i, end='->')
        while a[i] < pivot: i += 1
#        print(i)
#        print("j=",j, end='->')
        while a[j] > pivot: j -= 1
#        print(j)   
        if i < j:
            # Swap the elements
            a[i], a[j] = a[j], a[i]  
#            print(a)
            i += 1
#    print('\n')
    # Recur on the partitioned sections
    return QuickSort(a[:i]) + QuickSort(a[i:]) 

if __name__ == '__main__':
    # Testing
    from numpy.random import randint
    
    a = list(randint(20, size=40))
    #a = [5,2,7,4,9,2]
    b = QuickSort(a)
    a.sort()
    print(a==b)