# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 10:49:35 2021
Searching Algorithms
@author: promethustra
"""

def BinarySearch(arr, el):
    """Implementation of basic binary search algorithm, here implemented to
    find the index of element 'el' in the a sorted array of floats/ints 'arr'.
    The time complexity is O(log2(n))."""
    # The recursive solution is most intuitive.
    # In the null case of an empty list, return None?
    if len(arr) == 0: return None
    # First divid the array in 2
    pivot = int(len(arr)/2)
#    print(f"Found pivot {pivot}")
    # If the center is the disired element, we're done
    if arr[pivot] == el:
#        print(f"{arr[pivot]} = {el}, Returning {pivot}")
        return pivot
    # else if it's greater, we look for the element in the 1st half
    elif arr[pivot] > el:
#        print(f"{arr[pivot]} > {el}, Repeating search on {arr[:pivot]}")
        return BinarySearch(arr[:pivot], el)
    # and if it's smaller, we look in the second half
    elif arr[pivot] < el:
#        print(f"{arr[pivot]} < {el}, Repeating search on {arr[pivot:]}")
        return pivot + BinarySearch(arr[pivot:], el)

if __name__ == '__main__':
    
    a = [0, 2, 3, 6, 8, 9, 12, 13, 15, 18, 21, 24, 30, 42, 48, 50]
    
    for e in a:
        print(f"Searching for {e}: ", end='')
        i = BinarySearch(a, e)
        if a[i] == e: print("Success!")
        else: print("Failure.")