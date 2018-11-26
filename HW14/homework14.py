# imports {{{1
from __future__ import division
from copy import deepcopy, copy
from random import randrange
import heapq
#---------------------------------------------------------------------------}}}1

class priority_dict(dict):  # {{{1
  # A dictionary that maintains a heap with items in the dictionary sorted
  # according to the dictionary keys. It is a subclass of the dictionary class.
  # You can read about dictionaries here:
  #
  #   https://docs.python.org/2/library/stdtypes.html#typesmapping
  #
  # Methods from the dictionary superclass are inherited, but some might not
  # play nicely with the heap.
  #
  # Updating the keys is supported, which is the main benefit. We use a heap to
  # store the data, and a dictionary structure to store the (key, value)
  # association. Upon updating a key, we update the dictionary and add a
  # *duplicate* entry to the heap (or rebase if it has grown too large). This
  # saves O(n) on each operation until we have to rebase. When we pop from the
  # heap, we have to make sure that we're not getting a value with an outdated
  # key, so we check the dictionary to see if the keys match.
  #
  # priority_dict._heap -- the actual heap
  #
  # priority_dict._rebuild() -- rebuilds the heap
  #
  # priority_dict.pop() -- returns and removes the element with the least key
  # priority_dict.peek() -- returns and does not remove the element with the
  #   least key
  # priority_dict.push(value,key) -- adds the (key, value) pair to the heap
  # priority_dict.update_key(value,key) -- updates the key of value to new_key

  def __init__(self, *args, **kwargs):  # {{{
    # call the dictionary __init__ from the superclass
    super(priority_dict, self).__init__(*args, **kwargs)
    self._rebuild()  # sets up the heap
  # --------------------------------------------------------------------------}}}

  def _rebuild(self):  # {{{
    # The heap likes key to come before value, but we store it backwards in the
    # dictionary
    self._heap = [(key, value) for (value, key) in self.iteritems()]
    heapify(self._heap)   # O(n)
  # --------------------------------------------------------------------------}}}

  def pop(self):  # {{{
    # Raises exception if heap is empty
    # Get what we think the top of the heap is as a (key, value) pair. The
    # key that the dict holds should match, otherwise the key is outdated and
    # we should get the next item in the heap.

    key, value = heappop(self._heap)
    while value not in self or self[value] != key:
      key, value = heappop(self._heap)
    del self[value]
    return value
  # --------------------------------------------------------------------------}}}

  def peek(self):  # {{{
    # Raises exception if heap is empty.
    # See priority_dict.pop for a description of what's going on.

    key, value = self._heap[0]
    while value not in self or self[value] != key:
      heappop(self._heap)   # only throws away outdated (key, value) pairs
      key, value = self._heap[0]
    return value
  # --------------------------------------------------------------------------}}}

  def push(self, value, key):  # {{{
    # adds (key,value) to heap and to the dictionary

    heappush(self._heap, (key, value))
    self[value] = key
  # --------------------------------------------------------------------------}}}

  def update_key(self, value, key):  # {{{
    # Update the key for value. We don't remove it from the heap since this will
    # be O(n). Instead we update the key in the dictionary and add a duplicate
    # to the heap. If the heap is too big (2x the dictionary), then we rebuild
    # so that we aren't wasting memory.

    super(priority_dict, self).__setitem__(value, key)
    heappush(self._heap, (key, value))

    # rebuild the heap if it's too big
    if len(self._heap) >= 2*len(self):
      self._rebuild()
  # --------------------------------------------------------------------------}}}

  def __setitem__(self, value, key):  # {{{
    self.update_key(value, key)
  # --------------------------------------------------------------------------}}}
# ---------------------------------------------------------------------------}}}1


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
      del self.rev[t][s_index]
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
  def is_path(self, path): # {{{
    if not path:    # if path is [] or None
      return False

    for i in range(1, len(path)):
      if not self.has_edge(path[i-1], path[i]):
        return False
    return True
#----------------------------------------------------------------------------}}}
  def is_cycle(self, path): # {{{
    # in an undirected graph 1-cycles don't count
    if not self.directed and len(path) == 2:
      return False

    return self.is_path(list(path) + [path[0]])
#----------------------------------------------------------------------------}}}

  def in_degree(self, s): # {{{
    return len(self.rev[s])
  #--------------------------------------------------------------------------}}}
  def out_degree(self, s): # {{{
    return len(self.adj[s])
  #--------------------------------------------------------------------------}}}
  def degree(self, s): # {{{
    if not self.directed:
      return self.out_degree(s)

    return self.out_degree(s) + self.in_degree(s)
  #--------------------------------------------------------------------------}}}

  def sort(self): # {{{
    # Sort the adjacency lists
    for n in self.nodes:
      self.adj[n] = sorted(self.adj[n])
      self.rev[n] = sorted(self.rev[n])
  #--------------------------------------------------------------------------}}}
  def reverse(self): # {{{
    # returns reverse graph
    rev_adjlist = AdjList(len(self.nodes), directed = self.directed)
    rev_adjlist.adj = deepcopy(self.rev)
    rev_adjlist.rev = deepcopy(self.adj)

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

def rand_weight_graph(num_nodes):  # {{{
  phi = (1 + 5**0.5)/2
  num_edges = int( num_nodes*phi )
  min_weight = 1
  max_weight = num_nodes // 2

  G = AdjList(num_nodes)
  w = dict()
  for _ in xrange(num_edges):
    new_edge = (randrange(num_nodes), randrange(num_nodes))
    G.add_edge( *new_edge )
    w[new_edge] = w[new_edge[1], new_edge[0]] = randrange( min_weight, max_weight+1 )
  G.sort()

  return G, w
#----------------------------------------------------------------------------}}}

def shortest_path_recursive(G, w, s, t, M=[]): # {{{
  """
  G is the graph, w is the set of weights on the edges of G, s and t are nodes
  in G, and M is the memo for the function.
  Returns a pair (path, weight). path an array of nodes in G connected by edges
  with path[0] = s and path[-1] = t. weight is the sum of the edge weights in
  path. This path should be the least weight path joining s to t. If no path
  exists, return ([], 0).
  """

  if not M:
    # Initialize your memo here. It depends on your exact implementation, but
    # it should be something like
    M = [ None for _ in G ]
    M[s] = 0
  
  
  

  return [], 0
#----------------------------------------------------------------------------}}}
def shortest_path_iterative(G, w, s, t): # {{{
  M = [ None for _ in G ]
  dist = [ float('inf') for _ in G]
  M[s] = [s],0
  v = s
  H = priority_dict({n: float('inf') for n in G.nodes})
  H.update_key(s, 0)

  while v != t:
    min_dist = float('inf')
    min_path = []
    for u in G[v]:
      print "checking adj nodes, ",u, v
      pwv = w[(u,v)]
      if M[u] == None and u != v:
        print "M pwv at ", v, " = ", M[v][1], "w edge", v, u, " = ", w[(u,v)]
        pwv = M[v][1] + w[(u,v)]
        print "checking path weight val", pwv
        if pwv < min_dist:
          min_dist = pwv
          min_path = list(set().union([v],M[v][0],[u]))
          print " min path found to be ", min_path, " with weight ", min_dist
          next_node = u
    if next_node != v:
      v = next_node
      M[next_node] = min_path, min_dist
    else:
      v = M[v][0][-2]
    print M
    print v

  return M






#----------------------------------------------------------------------------}}}

# You should test your solution using something like this.
G, w = rand_weight_graph(10)#randrange(20))
s = randrange(len(G))
t = randrange(len(G))
print G
print w
print "(s,t) = ", (s, t)
# print shortest_path_recursive(G, w, s, t)
print shortest_path_iterative(G, w, s, t)
