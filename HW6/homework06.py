# imports {{{1
from __future__ import division
from collections import deque
from copy import deepcopy
from itertools import *
import math
from random import randrange
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

    #print "running is cycle on \n", path

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

def randgraph(num_nodes, directed=False):  # {{{
  phi = (1 + 5**0.5)/2
  num_edges = int( num_nodes*phi )

  G = AdjList(num_nodes, directed=directed)
  for _ in xrange(num_edges):
    new_edge = (randrange(num_nodes), randrange(num_nodes))
    G.add_edge( *new_edge )
  G.sort()
  return G
#----------------------------------------------------------------------------}}}
def topological_sort(G):  # {{{
  # Return a topological sort of G if it exists. Your algorithm should be
  # *linear* in (number of vertices + number of edges).
  S = []
  in_degrees = [ G.in_degree(s) for s in G.nodes ]
  in_degrees_0 = [ s for s in G.nodes if in_degrees[s] == 0 ]
  while len(in_degrees_0) != 0:
    v = in_degrees_0.pop()
    S.append(v)
    for u in G[v]:
      in_degrees[u] -= 1
      if in_degrees[u] == 0:
        in_degrees_0.append(u)
  return S
#----------------------------------------------------------------------------}}}
def is_DAG(G):  # {{{
  # Return true if G is a directed acyclic graph, and false otherwise.
  return len(topological_sort(G)) == len(G)
#----------------------------------------------------------------------------}}}

def rand_intervals(number, size = None): # {{{
  if size == None:
    size = int(math.ceil(number * 2**0.5))

  I = []
  count = 0
  while count < number:
    start = randrange(size-1)
    finish = randrange(start+1, size)
    if (start,finish) not in I:
      I.append( (start,finish) )
      count += 1
  return I
#----------------------------------------------------------------------------}}}
def sort_intervals_finish(I):  # {{{
  finish_key = lambda interval: interval[1]
  return sorted(I, key=finish_key)
#----------------------------------------------------------------------------}}}
def interval_scheduling(I): # {{{
  I_sorted = sort_intervals_finish(I)
  sched = [ I_sorted[0] ]
  for a in I_sorted:
    # if the start time of the current interval is after the finish time of the
    # last scheduled one, then add it
    if a[0] >= sched[-1][1]:
      sched.append(a)
  return sched
#----------------------------------------------------------------------------}}}
def depth(I): # {{{
  for d in range(len(I),0,-1):
    for subset in combinations(I,r=d):
      # The intersection of a bunch of intervals is the interval
      # ( max(start_times), min(finish_times) ). We just need to check that it
      # is nonempty.
      start_times = [ a[0] for a in subset ]
      finish_times = [ a[1] for a in subset ]
      if max(start_times) < min(finish_times):
        return d
#----------------------------------------------------------------------------}}}
def check_part(I, P):  # {{{
  # check that everything is in the partition
  if len(I) != sum( [len(part) for part in P] ):
    return False

  # check that we have the right number of parts
  if len(P) != depth(I):
    return False

  # check that the parts are compatible
  for part in P:
    if depth(part) != 1:
      return False
  return True

def filter_list(full_list, excludes):
  s = set(excludes)
  return (x for x in full_list if x not in s)
#----------------------------------------------------------------------------}}}


def findCycleDirHelper(G):  # {{{
  # By modifying the topological sort algorithm, find a cycle in the directed
  # graph G. Your algorithm should be linear in the nodes and edges of G. If G
  # is acyclic, return None. If G has a cycle, say 
  #   a1 -> a2 -> ... -> ak -> a1,
  # then return the list [a1, a2, ..., ak]. Loops of the form a1 -> a1 count as
  # 1-cycles, and 2-cycles of the form a1 -> a2 -> a1 count as well.
  S = []
  in_degrees = [ G.in_degree(s) for s in G.nodes ]
  in_degrees_0 = [ s for s in G.nodes if in_degrees[s] == 0 ]
  while len(in_degrees_0) != 0:
    v = in_degrees_0.pop()
    S.append(v)
    for u in G[v]:
      in_degrees[u] -= 1
      if in_degrees[u] == 0:
        in_degrees_0.append(u)
  return list(filter(lambda x: x not in set(S), G.nodes))

def findCycleDir(G):
  non_top_sort = findCycleDirHelper(G)
  out_degrees_0 = [ s for s in G.nodes if G.out_degree(s) == 0 or G.in_degree(s) == 0]
  possible_cycle_list = list(filter(lambda x: x not in set(out_degrees_0), non_top_sort))


  for i in range(0,len(possible_cycle_list) -1 ):
    for j in range(i+1,len(possible_cycle_list) -1 ):
      if G.is_cycle(possible_cycle_list[i:j]):
        return possible_cycle_list[i:j]

  return []
#----------------------------------------------------------------------------}}}
def getSecond(val): 
    return val[1]

def getFirst(val): 
    return val[0]

def isIntersecting((x,y),(a,b)):
    if  y > a:
      return True
    else:
      return False    

def interval_partitioning(I): # {{{
  # Solve the interval partioning problem for the list of intervals I. You
  # should return a partition of I in a certain format. If P is the partition,
  # then P[i] should be the list of intervals labeled with i. For example, if I
  # = [ (1,4), (2,6), (56)], [(1,6)] ], so intervals (1,4), (5,6) are labeled 0,
  # interval (2,6) is labeled ,6), (1,6) ], your returned partition might be P = [
  # [(1,4), (5,6)], [(2,1, and,6) is labeled 2.
  I.sort(key=getFirst)
  sched = [[]]
  for i in range(1,depth(I)):
    sched.append([])
  print sched
  new_label = True
  sched[0].append(I[0])
  label = 0
  for i in range(0, len(I)-1):
    if new_label:
      sched[label].append(I.pop(0))
      new_label = False

    for j in range(1,len(I)-1):
      print "checking intersection of  ", I[i], " and ", I[j]
      print "label = ", label, " len sched = ", len(sched), "sched at label = ", sched[label] 
      if not isIntersecting(sched[label][len(sched[label])-1],I[j]):
        print "not intersecting ", I[i], " and ", I[j]
        print "attempting to add to sched w label ", label
        sched[label].append(I.pop(0))
      else:
        new_label = True
        label += 1
        break
        

  return sched   # delete in your solution
#----------------------------------------------------------------------------}}}


# run this a few times to make sure your findCycleDir function is working
#A = randgraph(randrange(20), directed=True)
#C = findCycleDir(A)
#print A
#print C
#print A.is_cycle(C)

## you can run this to be more certain that your findCycleDir function works in
## general
##for _ in range(10**4):
#  A = randgraph(randrange(20), directed=True)
#  C = findCycleDir(A)
#  if C and ( not A.is_cycle(C) or is_DAG(A) ):
#    print "whoops"
#    print A
#@    print C
#    break


## check your interval_partitioning function by running this a couple times
I = rand_intervals(randrange(15))
print I
P = interval_partitioning(I)
for i,part in enumerate(P):
  print i, part
print check_part(I, P)

## you can run this to be more certain that your interval_partitioning function
## works in general
#for _ in range(10**3):
#  I = rand_intervals(randrange(15))
#  P = interval_partitioning(I)
#  if I and not check_part(I, P):
#    print "whoops"
#    print I
#    for i,part in enumerate(P):
#      print i, part
#    break
