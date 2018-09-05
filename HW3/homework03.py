# imports {{{1
from __future__ import division
from collections import deque
from copy import deepcopy
from random import randrange
#---------------------------------------------------------------------------}}}1

class AdjList: # {{{1
  # A class for the adjacency list representation of a graph.
  # Undirected graphs will have an edge (s,t) if and only if it has edge (t,s).
  # A directed graph might have edge (s,t) without having edge (t,s).

  # AdjList.adj is the actual adjacency list. 
  # AdjList.directed is a bool indicating whether the graph is directed.
  # AdjList.nodes is an array of the form range(n).

  # Edges may be specified on initialization or with the add_edge method.

  # If A is an AdjList, then...
  #   - A[i] is the adjacency list for node i
  #   - len(A) is the number of nodes in the graph, *not* the number of edges
  #   - str(A) is a "nicer" version of the adjacency list. It gets run when you
  #     explicity or implicityly convert A to a string (like with print).
  # These correspond to the last 3 class methods.

  def __init__(self, num_nodes, edges = [], directed = False): # {{{
    self.nodes = range(num_nodes)
    self.adj = [ [] for _ in self.nodes ]
    self.directed = directed

    for (s,t) in edges:
      self.add_edge(s,t)

    self.sort()
  #--------------------------------------------------------------------------}}}

  def add_edge(self, s, t, try_directed = True): # {{{
  # Adds an edge (s,t). If the graph is undirected, it adds edge (t,s) as well.
    if t not in self.adj[s]:
      self.adj[s].append(t)

    if not self.directed and try_directed:
      self.add_edge(t, s, try_directed = False)
  #--------------------------------------------------------------------------}}}
  def del_edge(self, s, t, try_directed = True): # {{{
  # Deletes an edge (s,t) if it exists. If the graph is undirected, it deletes
  # the edge (t,s) as well.
    try:
      t_index = self.adj[s].index(t)
      del self.adj[s][t_index]
    except ValueError:
      pass

    if not self.directed and try_directed:
      self.del_edge(t, s, try_directed = False)
  #--------------------------------------------------------------------------}}}

  def has_edge(self, s, t): # {{{
    return t in self.adj[s]
  #--------------------------------------------------------------------------}}}
  def degree(self, s): # {{{
    # return the degree of the node s
    return  # remove in your solution
  #--------------------------------------------------------------------------}}}
  def sort(self): # {{{
    # Sort the adjacency lists
    for n in self.nodes:
      self.adj[n] = sorted(self.adj[n])
  #--------------------------------------------------------------------------}}}

  def __getitem__(self, node):  # {{{
    return self.adj[node]
  #--------------------------------------------------------------------------}}}
  def __len__(self):  # {{{
    return len(self.nodes)
  #--------------------------------------------------------------------------}}}
  def __str__(self):  # {{{
    ret = ""
    for n in self.nodes:
      neighbors = [ str(i) for i in self.adj[n] ]
      ret += str(n) + ": " + " ".join(neighbors) + "\n"
    return ret[:-1]
  #--------------------------------------------------------------------------}}}
#----------------------------------------------------------------------------}}}1

def randgraph(num_nodes):  # {{{
  num_edges = int( num_nodes*2**0.5 )

  G = AdjList(num_nodes)
  for _ in xrange(num_edges):
    new_edge = (randrange(num_nodes), randrange(num_nodes))
    if not G.has_edge( *new_edge ):
      G.add_edge( *new_edge )
  G.sort()
  return G
#----------------------------------------------------------------------------}}}

def BFS(G, s):  # {{{
  # Breadth First search for G and s. Returns a BFS tree rooted at s. The data
  # structure deque is used. It is something like a symmetric queue, with O(1)
  # operations to add/pop elements from either end:
  # https://docs.python.org/2/library/collections.html#collections.deque

  seen = [ False for _ in G.nodes ]
  dist = [ -1 for _ in G.nodes ]

  seen[s] = True
  dist[s] = 0
  BFS_Tree = AdjList(len(G), directed=True)
  working_nodes = deque([s])
  while len(working_nodes) != 0:
    u = working_nodes.popleft()
    for v in G[u]:
      if not seen[v]:
        BFS_Tree.add_edge(u,v)
        seen[v] = True
        dist[v] = dist[u] + 1
        working_nodes.append(v)

  return BFS_Tree, dist
#----------------------------------------------------------------------------}}}

def DFS(G,s): # {{{
  # G is an AdjList representation of a graph and s is a node in the graph.
  # Return the Depth First Search tree for G and s.

  # if you need to make copies of an AdjList object A, use B = deepcopy(A).

  return DFS_Tree
#----------------------------------------------------------------------------}}}
