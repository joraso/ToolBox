# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:38:04 2021
Linked list algorithms
@author: Joe Raso
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, nex=None):
        self.val = val
        self.next = nex
        
def constructList(vals):
    """Construct a linked list of ListNode odjects from a regular python
    list, and return the head node."""
    # Current method is iterative, recursive soln also exists
    head = ListNode(val=vals.pop(0))
    current = head
    while len(vals) > 0:
        nex = ListNode(val=vals.pop(0))
        current.next = nex; current = nex
    return head

def deconstructList(head):
    """Take the head of a linked list of ListNode objects and reconstruct a
    normal Python list."""
    vals = []
    while head != None:
        vals.append(head.val)
        head = head.next
    return vals
    
def printList(head):
    """Prints out the values in a linked list of ListNode objects."""
    print(deconstructList(head))
    
def swapPairs(head): #: ListNode) -> ListNode:
    """Given a linked list, swap every two adjacent nodes and return its
    head."""
    # We could modify the node values, but instead let's rearrange the
    # connectivity of the nodes.
    
    # Null/terminal case
    if head == None:
        return None
    elif head.next == None:
        return head
    else:
        # perform the swap and recur:
        newhead = head.next
        head.next = swapPairs(head.next.next)
        newhead.next = head
        print(newhead.val)
        return newhead
        
def reverseList(head):
    """Reverse a singly linked list."""
    def inout(node):
        # we'll need to pass the new head of the list back to the
        # parent function:
        nonlocal head
        # Terminate if this is the null case, or we've reccured to the
        # end of the list:
        if node == None or node.next == None:
            head = node # pass the new head to the outer namespace.
            return node # pass up the tail of the reversed list
        # If this is not the end of the list, we recur until we find it, then
        # reverse-link the nodes (imagine turning a sock inside out).
        else:
            link = inout(node.next)
            node.next = None # unlink to avoid circular logic
            link.next = node # relink in reverse
            return node # pass up the tail of the reversed list
    inout(head)
    return head
        
if __name__ == "__main__":
    a = constructList([1,2,3,4,5,6])
    printList(a)
    #a = swapPairs(a)
    a = reverseList(a)
    printList(a)