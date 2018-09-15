# imports {{{1
from __future__ import division
from copy import deepcopy
from random import randrange
from collections import deque

from sys import *
#---------------------------------------------------------------------------}}}1
class AdjList: # {{{1
  # A class for the adjacency list representation of a graph.
  # Undirected graphs will have an edge (s,t) if and only if it has edge (t,s).
  # A directed graph might have edge (s,t) without having edge (t,s).

  # AdjList.adj is the actual adjacency list.
  # AdjList.rev is the adjacency list of the reverse graph
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
    self.rev = [ [] for _ in self.nodes ]
    self.directed = directed

    for (s,t) in edges:
      self.add_edge(s,t)

    self.sort()
  #--------------------------------------------------------------------------}}}

  def add_edge(self, s, t, try_directed = True): # {{{
  # Adds an edge (s,t). If the graph is undirected, it adds edge (t,s) as well.
    if t not in self.adj[s]:
      self.adj[s].append(t)
      self.rev[t].append(s)

    if not self.directed and try_directed:
      self.add_edge(t, s, try_directed = False)
  #--------------------------------------------------------------------------}}}
  def del_edge(self, s, t, try_directed = True): # {{{
  # Deletes an edge (s,t) if it exists. If the graph is undirected, it deletes
  # the edge (t,s) as well.
    try:
      t_index = self.adj[s].index(t)
      del self.adj[s][t_index]
      s_index = self.rev[t].index(s)
      del self.adj[t][s_index]
    except ValueError:
      pass

    if not self.directed and try_directed:
      self.del_edge(t, s, try_directed = False)
  #--------------------------------------------------------------------------}}}

  def has_edge(self, s, t): # {{{
    return t in self.adj[s]
  #--------------------------------------------------------------------------}}}
  def has_edge_rev(self, s, t): # {{{
    return t in self.rev[s]
  #--------------------------------------------------------------------------}}}
  def degree(self, s): # {{{
    if not self.directed:
      return len(self.adj[s])

    out_deg = len(self.adj[s])
    in_deg = len(self.rev[s])
    return out_deg + in_deg
  #--------------------------------------------------------------------------}}}
  def sort(self): # {{{
    # Sort the adjacency lists
    for n in self.nodes:
      self.adj[n] = sorted(self.adj[n])
      self.rev[n] = sorted(self.rev[n])
  #--------------------------------------------------------------------------}}}

  def reverse(self): # {{{
    # returns reverse graph
    rev_adjlist = AdjList(self.nodes, directed = self.directed)
    rev_adjlist.adj = deepcopy(self.adj)
    rev_adjlist.rev = deepcopy(self.rev)

    return rev_adjlist
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
def predecessors(BFS_Tree, u, stop_at=None): # {{{
  # Return an array of predecessors of u in the BFS tree. The last element will
  # be the root, and the first will be u. If stop_at is specified, then stop at
  # that ancestor instead of the root of the tree

  preds = [u]
  parent = u
  while len(BFS_Tree.rev[parent]) != 0 and parent != stop_at:
    print "len of BFS_tree rev at parent ", len(BFS_Tree.rev[parent])
    parent = BFS_Tree.rev[parent][0]
    print "parent set to ", parent
    preds.append(parent)
  return preds
#----------------------------------------------------------------------------}}}
def common_ancestor_paths(BFS_Tree, u, v): # {{{
  # The nodes u and v have a common ancestor, call it c. Function returns a pair
  # of arrays U, V such that U is a path in BFS_Tree from u to c and V is a path
  # in BFS_Tree from v to c.

  preds_u = predecessors(BFS_Tree, u)
  preds_v = predecessors(BFS_Tree, v)
  while len(preds_u) != 0 and len(preds_v) != 0 and preds_u[-1] == preds_v[-1]:
    common_ancestor = preds_u.pop()
    preds_v.pop()

  path_u_common_ancestor = predecessors(BFS_Tree, u, stop_at=common_ancestor)
  path_v_common_ancestor = predecessors(BFS_Tree, v, stop_at=common_ancestor)

  return path_u_common_ancestor, path_v_common_ancestor
#----------------------------------------------------------------------------}}}
def is_cycle(G, seq): # {{{
  if len(seq) == 0 or len(seq) == 2:
    return False

  prev_node = seq[0]
  for i in range(1, len(seq)):
    cur_node = seq[i]
    if not G.has_edge(prev_node, cur_node):
      return False
    prev_node = cur_node
  return G.has_edge(seq[-1], seq[0])
#----------------------------------------------------------------------------}}}

def findCycle(G): # {{{
  # Find a cycle in undirected G if it exists. If one is found, return an array
  # of the nodes in the cycle. If one is not found, return the python value
  # None. For example, if we have a 5-cycle 1 -- 0 -- 5 -- 6 -- 1, then return
  # [1,0,5,6] (or any cyclic permutation of this list). A loop 1 -- 1 is a
  # 0-cycle and you should return [1]. Things like 1 -- 2 -- 1 don't count as
  # cycles since you have to take the same edge back to 1. 

  # You may want to base your algorithm on the BFS function above, and I suggest
  # using the functions predecessors and common_ancestor_paths.
  # Mark all the vertices as not visited
        visited =[False]*(len(G.nodes))
        cyc = []
        # Call the recursive helper function to detect cycle in different
        #DFS trees
        for i in range(len(G.nodes)):
            if visited[i] ==False: #Don't recur for u if it is already visited
              isCyclicUtil(G,i,visited,-1,cyc)

        if cyc != []:
          cyc.pop()        
          return cyc
        else:
          return None

 
#----------------------------------------------------------------------------}}}

def isCyclicUtil(G,v,visited,parent,cyc):
 
        #Mark the current node as visited 
        visited[v]= True
        #Recur for all the vertices adjacent to this vertex
        for i in G.adj[v]:
            # If the node is not visited then recurse on it
            if  visited[i]==False : 
                if(isCyclicUtil(G,i,visited,v,cyc)):
                    cyc.append(i)
                    return cyc
            # If an adjacent vertex is visited and not parent of current vertex,
            # then there is a cycle
            elif  parent!=i:
                cyc.append(i)
                return cyc
         
        return None

def randgraph(num_nodes):  # {{{
  phi = (1 + 5**0.5)/2
  num_edges = int( num_nodes*phi )

  G = AdjList(num_nodes)
  for _ in xrange(num_edges):
    new_edge = (randrange(num_nodes), randrange(num_nodes))
    if not G.has_edge( *new_edge ):
      G.add_edge( *new_edge )
  G.sort()
  return G
#----------------------------------------------------------------------------}}}

# You can check your findCycle implementation by running this several times and
# checking the output:
# A = randgraph(randrange(25))
A = AdjList(5)
A.add_edge(0,1)
A.add_edge(0,2)
A.add_edge(2,3)
A.add_edge(2,4)
A.add_edge(3,4)
print A
C = findCycle(A)
print C
exit()

# Once you think your implementation works in general, you might try automating
# the above test with this:
for _ in xrange(10**5):
  A = randgraph(randrange(25))
  C = findCycle(A)
  if C is not None and not is_cycle(A, C):
    print A, C
    break
exit()
