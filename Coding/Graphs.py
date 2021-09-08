# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:36:07 2021
Collection of graph structures and algorithms.
@author: promethustra
"""

class Node:
    """Object for a node in a general graph. The node has a value (mandatory),
    and some number of paths (optional at instantiation) to other nodes in the
    graph. Bi-directional graphs can be realized by giving connected nodes
    mutual paths to each other."""
    def __init__(self, value, paths=None):
        self.value = value
        # It has to be done this way to avoid making paths a class variable
        # this is true because lists are mutable.
        self.paths = [] if paths == None else paths
    def __repr__(self):
        return f"Node {self.value}"
        
class Graph:
    """Object for a graph of nodes. Initialized with a list of node values and
    a list of edges; an edge is indicated by a tuple of ints < n_nodes, with
    (index of source node, index of destination node). The graph and edges
    are directed by default; If an undirected graph is indicated, the reverse
    of each edge is added as well."""
    def __init__(self, values, edges, directed=True):
        self.nodes = [Node(value) for value in values]
        for edge in edges:
            if edge[0]<len(self.nodes) and edge[1]<len(self.nodes):
                # Add edge paths to nodes if the edge coords are valid
                self.nodes[edge[0]].paths.append(self.nodes[edge[1]])
                if not directed:
                    # If the graph isn't directed, also add the reverse edge
                    self.nodes[edge[1]].paths.append(self.nodes[edge[0]])
            else:
                print(f"Error: Connection {edge} cannot be formed", end=': ')
                print("node index out of range.")
    def summary(self):
        """Prints a summary of the nodes and their connections."""
        for node in self.nodes:
            print(f"{node} -> {node.paths}")
            
    def DepthFirstSearch(self, value, head=0):
        """Performs a depth-first search of the graph for 'value'. Defaults
        to starting at node 0. Returns the node containing the value and an
        integer indicating the path length. Note that this DOES NOT find the
        shortest path (necessarily)."""
        pathlen = 0; visited = []
        def search(node, value, pathlen):
            # Check if this node has been visited. If not, add it to the list
            nonlocal visited
            if node in visited: return None
            else: visited.append(node)
            # If this node has the value we want, return it's info
            if node.value == value:
                return node, pathlen
            # Otherwise continue to search the children
            else:
                for child in node.paths:
#                    print(f"continuing to {child}")
                    result = search(child, value, pathlen+1)
                    if result == None: continue
                    else: return result
        # Recur to find the path, starting at the indicated head.
        return search(self.nodes[head], value, pathlen)
        
    def BreadthFirstSearch(self, value, head=0):
        """Performs a breadth-first search of the graph for 'value'. Defaults
        to starting at node 0. Returns the node containing the value and an
        integer indicating the path length. Note that this DOES find the
        shortest path."""
        pathlen = 0; visited = []
        queue = [self.nodes[0]]; nexqueue = []
        while len(queue) > 0:
            print(f"visiting {queue}")
            while len(queue) > 0:
                # Take a node off the queue to test
                node = queue.pop(0)
                # Disregard it if we've visited it already
                if node in visited: continue
                else: visited.append(node) 
                # and return if it's what we're looking for
                if node.value == value: return node, pathlen
                # otherwise add it's children to the list to check
                else: nexqueue += node.paths
            # if the value was not in that layer of nodes, increment pathlen
            # and move on to the next layer of nodes.
            queue = nexqueue; nexqueue = []; pathlen += 1
        return None
        
    def FindIslands(self):
        """Finds all the islands of interconnected nodes on the graph
        returning a list of lists of nodes."""
        # The way to accomplish this will be with depth-first search
        notvisited = self.nodes.copy(); island = []
        def explore(node):
            nonlocal notvisited, island
            # Proceed only if we have never been to this node.
            if node in notvisited:
                # Mark as visited
                notvisited.remove(node)
                island.append(node)
                # and explore it's connections
                for child in node.paths:
                    explore(child)
        # Explore all the islands
        islands = []
        while len(notvisited)>0:
            explore(notvisited[0])
            islands.append(island.copy())
            island = []
        return islands


if __name__ == '__main__':
    
#    g = Graph(['A','B','C','D'],[(0,1),(0,2),(1,2),(2,3)], directed=False)
#    g.summary()
#    result = g.DepthFirstSearch('D')
#    result = g.BreadthFirstSearch('D')
#    print(result)
    
    g2 = Graph(['A','B','C','D', 'E', 'F'],
               [(1,2),(3,4),(4,5),(5,3)], directed=False)
    g2.summary()
    print(g2.FindIslands())