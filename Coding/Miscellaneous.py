# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:04:15 2021
Miscellanious coding problems I find interesting (or frustrating).
@author: Joe Raso
"""

import datetime

# Problems that gave me complexity headaches ==================================

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

# Problems that are good to remember ==========================================

def reverseString(s): #: List[str]) -> None
    """A simple function to efficiently reverse a string, treated as a list of
    printable characters. Does not return anything, instead modifies the string
    in-place. """
#    # Here is one way:
#    end = len(s)-1
#    def swap(place):
#        nonlocal end
#        # If we're not at the endo of the list,
#        # continue bumping the character down
#        if place < end:
#            c = s.pop(place)
#            s.insert(place+1, c)
#            swap(place+1)
#        # If the character has reached it's final position
#        # adjust the endpoint and start from the top
#        # (as long as we haven't reached the terminal
#        # case where end==0.)
#        elif place == end:
#            end -= 1
#            if end > 0:
#                swap(0)
#    swap(0)
#    # This is too long in time though, O(n^2)
                
    # Here is another way that should work and be O(n):
    # Make the endpoint is the middle of the list:
    end = int(len(s)/2)-1
    # Null escape:
    if end < 0:
        return
    def swap(place):
        nonlocal end
        # Switch to characters in the string
        c1 = s[place]; c2 = s[-place-1]
        s[place] = c2; s[-place-1] = c1
        # Recur if we're not at the middle yet:
        if place < end:
            swap(place+1)
    swap(0)
    
# Problems that gave me design headaches ======================================

def knightlOnAChessboard(n):
    """KnightL(i,j) is a chess piece that moves in an L-shape according
    to integers i and j. This challenge is two-fold:
        1. Enumerate the KnightL(i,j) pieces that are possible on a 
           square board of side length n,
        2. For each possible KnightL, find the minimum number of moves
           to cross th board diagonally, from (0,0) to (n-1, n-1).
    should return a nested nxn array containing the minimum number of moves
    mentionen in (2); result[i,j] = minimum moves of KnightL(i,j) on
    the board of side length n."""
    
    # The duel nature of this problem gave took me a long time to solve.
    # Mainly, the design challenge lay in finding the way to calculate
    # minmoves() --- which I solved with some stat-mech like thinking.
    # My solution just advances all possible trajectories that don't 
    # include backtracking to a space already visited until either the
    # end space is reached (and we've arrived in the minimum number of 
    # moves or no more valid moves exist (there is no solution).
    
    # The secondary part --- avoiding recalculating minmoves() for redundant
    # KnightL combinations was also a bit of a head-scratcher without using,
    # numpy, but I think what came up with is this is an example of what
    # people call 'dynamic programming'?
    
    # First some component functions
    def onboard(space, n):
        """Define whether a given set of coordinates are on a board of side
        length n."""
        return (space[0]<n and space[1]<n and space[0]>=0 and space[1]>=0)
    def minmoves(i, j, n):
        """Find the minimum number of moves across the board of side length 
        n with KnightL(i, j)"""
        # There are 8 possible moves for the knight in the middle of the board
        moves = [(i, j), (j, i), (-i, j), (j, -i),
                 (i, -j), (-j, i), (-i, -j), (-j, -i)]
        # Track the current location(s) of the trajectories
        # The spaces already visited (to avoid loops)
        # and the number of steps in the current set of trajectories
        locs = [(0,0)]; visited =[]; steps = 0
        # grow trajectories until a solution is found
        while True:
#            print(f"Step {steps}")
            nextlocs = []
            for loc in locs:
                for m in moves:
                    s = (loc[0]+m[0], loc[1]+m[1])
                    # check if these next steps are:
                    # (a) possible and/or (b) not already visited
                    if onboard(s, n) and (s not in visited):
                        # if so, progress the trajectories to the new location
                        nextlocs.append(s); visited.append(s)
#                        print(f"{loc}->{s}")
            # progress all trajectories one step
            locs = nextlocs; steps += 1
            # check if any have reacked the target location
            if (n-1, n-1) in locs:
                return steps
            # if all trajectories have moved off the board,
            # no solutions exist.
            elif len(locs) == 0:
                return -1
    # Initiate the result matrix with zeros
    result = []
    # enumerate all possible KnightL objects on board of size n
    # note that KnightL(i,j)=KnightL(j,i), so we can reuse values 
    for i in range(1, n):
        line = []
        for j in range(1, i):
#            print(f"Filling at {i}, {j}")
            line.append(result[j-1][i-1])
        for j in range(i, n):
#            print(f"Calculating at {i}, {j}")
            m = minmoves(i, j, n)
            line.append(m)
        result.append(line)
#        print(result)
    return result

    
if __name__ == "__main__":
    
    # Troubleshooting 3sum
    # The problem children inputs:
#    nums = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
#            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
#            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#    nums = [0,0,0]      
#    nums = [0,0,0,0]
#    nums = [-2,0,1,1,2]
#    tic = datetime.datetime.now()
#    print(threeSum(nums))
#    toc = datetime.datetime.now()
#    elapsed = float((toc-tic).total_seconds())
#    print("Time Elapsed: {} seconds".format(elapsed))

    # Troubleshooting reverse string
#    a=[1,2,3,4,5,6,7]
#    reverseString(a)
#    print(a)

    # Troubleshooting knightlOnAChessboard()
    r = knightlOnAChessboard(5)
    ans = [[4, 4, 2, 8], [4, 2, 4, 4], [2, 4, -1, -1], [8, 4, -1, 1]]
    print(ans==r)
    # An