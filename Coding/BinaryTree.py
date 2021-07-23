# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:07:21 2021
@author: Joe Raso
"""

# Definition for a binary tree node.
class TreeNode:
    """Base class for binary tree nodes.
    Attributes:
    val   - (any) the value stored in the node.
    left  - (TreeNode) Link to the left branch.
    right - (TreeNode) Link to the right branch."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class BinaryTree:
    """Binary Tree object."""
    def __init__(self):
        self.root = TreeNode() # default to an empty root node
    def Traverse(self, order="pre"):
        """Combination function for various methods of traversing the tree.
        Keywords:
        order - (string) Specifies the ordering of the traversal. Options are
                ['pre', 'in', 'post'], standing for preorder, inorder and post-
                order respectively.
        Returns:
        ordered - (list) List of node values, returned in the specified order.
        """
        # Good to do an input check/escape
        if order not in ['pre', 'in', 'post']:
            print("Invalid order presented."); return []
        ordered = []
        def travel(node):
            # recursive subruetine for traversing the tree. all methods
            # actually travese through nodes in the same left-to-right
            # progression, and are only distinguished by when node values
            # are added to the list:
            if order=="pre":             # preordering adds the node the
                ordered.append(node.val) # first time the algorithm sees it.
            # <traverse the left branch>
            if node.left != None:         
                travel(node.left)
            if order=="in":              # inordering adds the node after the
                ordered.append(node.val) # the left branch has been explored.
            # <traverse the right branch>
            if node.right != None:
                travel(node.right)
            if order=="post":            # postordering adds the node after
                ordered.append(node.val) # all its branches have been explored.
        if self.root == None:
            return [] # Null case is unlikely, but possible?
        else:
            travel(self.root)
            return ordered
    def buildTree(self, inorder, postorder):
        """Builds the tree (self) based on inorder and postorder lists. 
        Importent: this function implicilty assumes duplicate node values do 
        not exist, and it may mis-behave if attepting to build such a tree with
        duplicate node values.
        Arguments:
        inorder   - (list) The inorder node values.
        postorder - (list) The postorder node values."""
        def build(inorder, postorder):
            # Escape case when passed an empty list,
            if len(postorder)==0:
                return None
            # Identify where the root node (of this branch) is in the inorder 
            # by looking at the postorder (where root node is always last).
            newnode = TreeNode(val=postorder[-1]); n = -1
            for i in range(len(inorder)):
                if inorder[i] == newnode.val:
                    n = i
            # Now we can divide the lists into the in/preorder of each branch
            # off the current node to recur further down the tree:
            # inorder   = [left branch] [root] [rightbranch]
            # postorder = [left branch] [right branch] [root]
            # note that the lengths of each branch list are the same.
            newnode.right = build(inorder[n+1:], postorder[n:-1])
            newnode.left = build(inorder[:n], postorder[:n])
            # return the branch or sub-branch up the recursion chain:
            return newnode
            # Thanks to leetcode user @ tr1cky for the guide!
        self.root = build(inorder, postorder)
    def maxDepth(self):
        """Return the maximum root-to-leaf depth.
        Returns:
        depth - (int) Maximum root-to-leaf depth"""
        # I think this recursive method is called "bottom up"? There should
        # also be a topdown solution.
        def depth(node):
            # For each branch of the current node/recursion level, seach down
            # the tree if that branch exists:
            if node.left != None:
                left = 1 + depth(node.left)
            else:
                left = 0
            if node.right != None:
                right = 1 + depth(node.right)
            else:
                right = 0
            # if neither branch exists, we're at a leaf:
            if node.left==None and node.right==None:
                return 1
            # otherwise, pass the greater of the two branch depths up to the
            # call/recusion level at the parent node.
            else:
                return max(left, right)
        if self.root == None:
            return 0 # Null case is unlikely, but possible?
        else:
            return depth(self.root)
    def isSymmetric(self):
        """Checks whether the tree is a mirror of itself (ie, symmetric around
        its center).
        Returns:
        symmetric - (bool) True if the tree is symmetric, false otherwise."""
        # We'll do this by pseudo-preordering the two main branches off the
        # root. The left branch will be normal preordered, but the right
        # will be reverse-preordered. Null connections will also be recorded
        # in order to preserve the directionality/shape of the tree.
        def left_preorder(node, tally):
            tally.append(node.val)
            if node.left != None:
                left_preorder(node.left, tally)
            else:
                tally.append(None) 
            if node.right != None:
                left_preorder(node.right, tally)
            else:
                tally.append(None)
        def right_preorder(node, tally):
            tally.append(node.val)
            if node.right != None:
                right_preorder(node.right, tally)
            else:
                tally.append(None)
            if node.left != None:
                right_preorder(node.left, tally)
            else:
                tally.append(None)
        # Null case first, again unlikely but possible.
        if self.root == None:
            return True
        # Then, search only of both secondary nodes exist
        elif self.root.right!=None and self.root.left!=None:
            leftbranch = []; left_preorder(self.root.left, leftbranch)
            rightbranch = []; right_preorder(self.root.right, rightbranch)
            # if the tree is symmetric, then the left preorder and the right
            # reverse preorder (including the placement of Null nodes should
            # be exactly equal.
            return leftbranch==rightbranch 
        # If one or both of the secondary nodes do not exist
        else:
            # Return False if only one exists, and True if neither does
            return not (self.root.right!=None or self.root.left!=None)
    def hasPathSum(self, targetSum):
        """Find out if there exists a root-to-leaf path that exactly equals 
        the target sum. Important: only work if the tree node values all have
        types that support addition (and that match the type of the target
        sum) --- Currently, this supports int, str, float and likely numpy
        array (untested), but may need to be modified for others.
        Arguments:
        targetSum - (*) the target sum to check for. Must match the data type
                    of the node values.
        Returns:
        SumExists - (bool) The existance of a root-to-leaf sum that equals the
                    target sum"""
        nullvalue = "" if type(targetSum)==str else 0
        SumExists = False
        def pathfinder(node, sofar):
            nonlocal SumExists
            # Add the current node value to our running sum.
            hereSum = sofar+node.val
            # Pass down each branch if it exists.
            if node.left != None:
                pathfinder(node.left, hereSum)
            if node.right != None:
                pathfinder(node.right, hereSum)
            # If niether branch exists, we are at a leaf, and we check to
            # see if the sum here is equal to the target value.
            if node.left==None and node.right==None and hereSum==targetSum:
                SumExists=True
        if self.root==None:
            return False # Null case is unlikely, but possible?
        else:
            pathfinder(self.root, nullvalue)
            return SumExists
            
if __name__ == '__main__':
    # Tests:
    
    # First trial: non-duplicate with integer values
    tree1 = BinaryTree()
    tree1.buildTree([4,2,5,1,6,3,7],[4,5,2,6,7,3,1])
#    tree1.isSymmetric() # Should be false
    
    # Second trial: duplicate, symmetric with char values
    tree2 = BinaryTree()
    # Build manually:
    tree2.root.val = 'd'
    tree2.root.left = TreeNode(val='a',
            left = TreeNode(val='d'),
            right = TreeNode(val='b',
                left = TreeNode(val='s')))
    tree2.root.right = TreeNode(val='a',
            right = TreeNode(val='d'),
            left = TreeNode(val='b',
                right = TreeNode(val='s')))