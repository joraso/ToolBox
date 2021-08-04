# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 19:49:41 2021
Sorting algorithms
@author: Joe Raso
"""

def QuickSort(a):
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

def MergeSort(a):
    """Implementation of mergesort algorithm for a python list of integers,
    sorting into ascending values. Runs at O(n*log2(n)) in the worst case.
    (but what is the worst case?)"""
    # Null / short list escape
    if len(a) < 2:
        return a
    # Perform the splitting and recur:
    idx = int(len(a)/2)
#    print(f"splitting {a} at index {idx}.")
    a1 = MergeSort(a[:idx])
    a2 = MergeSort(a[idx:])
    # merging into c
#    print(f"Merging {a1} and {a2} into ", end='')
    c = [] 
    # While both lists are non-empty, build c
    # by adding the lesser of the leading elements
    while len(a1)>0 and len(a2)>0:
        if a1[0] <= a2[0]:
            c.append(a1.pop(0))
        else:
            c.append(a2.pop(0))
    # if elements remain in either list, add them
    if len(a1)>0: c += a1
    if len(a2)>0: c += a2
#    print(c)
    return c
    

if __name__ == '__main__':
    # Testing
    from numpy.random import randint
    
    a = list(randint(20, size=40))
    #a = [5,3,2,7,4,8,6,1]
    #b = QuickSort(a)
    b = MergeSort(a)
    a.sort()
    print(a==b)