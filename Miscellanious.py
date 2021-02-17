# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:04:15 2021
Miscellanious coding problems I find interesting (or frustrating).
@author: Joe Raso
"""

import datetime

def threeSum(nums):#: list[int]) -> list[list[int]]:
    """Given an array nums of n integers, are there elements a, b, c in nums
    such that a + b + c = 0? Find all unique triplets in the array which gives
    the sum of zero. Notice that the solution set must not contain duplicate
    triplets."""    
    
    # This problem gave me so much greif, it's unbelievable.    
    
    # Iterative solution is conceptually the easiest ---
    # Number partition (i.e. this problem) doesn't generally
    # Have an analysical solution we can rely on.
    
    # Unfortunately, iterating through all possible 3-number
    # combintations is way, way to slow for long lists,
    # so we need to be more clever about it.
    
    combos = [] # The empty list
    nums.sort() # start by sorting
    
    # null exit
    if len(nums) < 3:
        return []

    for i in range(len(nums)-2):
        # Skip ahead in the case of long strings of identical digits,
        # we really don't need more than 3 (if they're all 0)
        if len(nums)>i+4 and nums[i] == nums[i+3]:
            continue
        # given the first number, zero in on the second and third
        j, k = i+1, len(nums)-1
#        print(i,j,k)
        while j < k:
#            print(j,k)
            s = nums[i]+nums[j]+nums[k]
            # if the sum is greater than zero, the third number is too high
            if s > 0:
                k -= 1
            # if the sum is less than zero, the second number is too low
            elif s < 0:
                j += 1
            # otherwise, we've found a solution:
            else:
                c = [nums[i],nums[j],nums[k]]
                # scrub for uniqueness. There should be a way to do this
                # with reference only to the indeces, but whatevs
                if c not in combos: 
                    combos.append(c)
                # and we want to restart the search with a new second number
                # ...and we can advance to where the next two are the same
                # also, we know that advancing j only increases the number,
                # so we don't have to reset k:
                j += 1
                while len(nums)>j+3 and j < k and nums[j]==nums[j+2]:
#                    print(j, k)
                    j += 1
                
    return combos
    
if __name__ == "__main__":
    # The problem children inputs:
#    nums = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
#            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
#            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#    nums = [0,0,0]      
    nums = [0,0,0,0]
#    nums = [-2,0,1,1,2]
    
    tic = datetime.datetime.now()
    print(threeSum(nums))
    toc = datetime.datetime.now()
    elapsed = float((toc-tic).total_seconds())
    print("Time Elapsed: {} seconds".format(elapsed))
