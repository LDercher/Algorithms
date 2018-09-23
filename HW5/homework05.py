# imports {{{1
from __future__ import division
from copy import deepcopy
from itertools import *
import math
from random import randrange
from sys import *
# ---------------------------------------------------------------------------}}}1


class AdjList:  # {{{1
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

    def __init__(self, num_nodes, edges=[], directed=False):  # {{{
        self.nodes = range(num_nodes)
        self.adj = [[] for _ in self.nodes]
        self.rev = [[] for _ in self.nodes]
        self.directed = directed

        for (s, t) in edges:
            self.add_edge(s, t)

        self.sort()
    # --------------------------------------------------------------------------}}}

    def add_edge(self, s, t, try_directed=True):  # {{{
        # Adds an edge (s,t). If the graph is undirected, it adds edge (t,s) as well.
        if t not in self.adj[s]:
            self.adj[s].append(t)
            self.rev[t].append(s)

        if not self.directed and try_directed:
            self.add_edge(t, s, try_directed=False)
    # --------------------------------------------------------------------------}}}

    def del_edge(self, s, t, try_directed=True):  # {{{
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
            self.del_edge(t, s, try_directed=False)
    # --------------------------------------------------------------------------}}}

    def has_edge(self, s, t):  # {{{
        return t in self.adj[s]
    # --------------------------------------------------------------------------}}}

    def has_edge_rev(self, s, t):  # {{{
        return t in self.rev[s]
    # --------------------------------------------------------------------------}}}

    def is_path(self, path):  # {{{
        if not path:    # if path is [] or None
            return False

        for i in range(1, len(path)):
            if not self.has_edge(path[i-1], path[i]):
                return False
        return True
# ----------------------------------------------------------------------------}}}

    def is_cycle(self, path):  # {{{
        # in an undirected graph 1-cycles don't count
        if not self.directed and len(path) == 2:
            return False

        return self.is_path(list(path) + [path[0]])
# ----------------------------------------------------------------------------}}}

    def in_degree(self, s):  # {{{
        return len(self.rev[s])
    # --------------------------------------------------------------------------}}}

    def out_degree(self, s):  # {{{
        return len(self.adj[s])
    # --------------------------------------------------------------------------}}}

    def degree(self, s):  # {{{
        if not self.directed:
            return self.out_degree(s)

        return self.out_degree(s) + self.in_degree(s)
    # --------------------------------------------------------------------------}}}

    def sort(self):  # {{{
        # Sort the adjacency lists
        for n in self.nodes:
            self.adj[n] = sorted(self.adj[n])
            self.rev[n] = sorted(self.rev[n])
    # --------------------------------------------------------------------------}}}

    def reverse(self):  # {{{
        # returns reverse graph
        rev_adjlist = AdjList(len(self.nodes), directed=self.directed)
        rev_adjlist.adj = deepcopy(self.adj)
        rev_adjlist.rev = deepcopy(self.rev)

        return rev_adjlist
    # --------------------------------------------------------------------------}}}

    def __getitem__(self, node):  # {{{
        return self.adj[node]
    # --------------------------------------------------------------------------}}}

    def __len__(self):  # {{{
        return len(self.nodes)
    # --------------------------------------------------------------------------}}}

    def __str__(self):  # {{{
        ret = ""
        for n in self.nodes:
            neighbors = [str(i) for i in self.adj[n]]
            ret += str(n) + ": " + " ".join(neighbors) + "\n"
        return ret[:-1]
    # --------------------------------------------------------------------------}}}
# ----------------------------------------------------------------------------}}}1


def bad_findCycle(G):  # {{{
    # Badly find (and return) a cycle in a directed or undirected graph. This is
    # a Theta(n*2^n) algorithm.

    # For directed graph, a 0 cycle is a loop, 1-cycles don't count. For
    # undirected, 1 cycles *do* count.
    if G.directed:
        cycle_lengths = range(len(G))
    else:
        cycle_lengths = [0] + range(2, len(G))

    for cycle_len in cycle_lengths:
        # Generate all permutations of length cycle_len+1 with entries from G.nodes.
        # For each one, check if it is a cycle.
        for cycle_candidate in permutations(G.nodes, cycle_len+1):
            if G.is_cycle(cycle_candidate):
                return list(cycle_candidate)

    return None   # no cycle found
# ----------------------------------------------------------------------------}}}


def bad_is_DAG(G):  # {{{
    return bad_findCycle(G) == None
# ----------------------------------------------------------------------------}}}


def bad_findHamiltonian(G):  # {{{
    # Badly find (and return) a Hamiltonian path in G.

    # Generate all permutations of G.nodes (full permutations). For each one,
    # check if it is a path.
    for h_candidate in permutations(G.nodes, len(G.nodes)):
        if G.is_path(h_candidate):
            return list(h_candidate)
    return None
# ----------------------------------------------------------------------------}}}


def find_in_deg_zero(G):
    for i in range(len(G.adj)):
        if G.in_degree(i) == 0:
            return i

    return None


def topological_sort(G):  # {{{
        # Return a topological sort of G if it exists. This should be a list of the
        # vertices of G arranged in the topological order. Your algorithm should be
        # *linear* in (number of vertices + number of edges). The class AdjList has
        # some new methods that you might find useful.
    seen = [False for _ in G.nodes]
    stack = []
    for i in range(len(G.adj)):
      if not seen[i]:
        top_sort_helper(G,i,seen,stack)
    
    return stack
    
#------------------------------------------------}}}


#assumes is will get an apudated graph with a deg 0 node
def top_sort_helper(G,v,seen,stack):
  seen[v] = True
  for i in G.adj[v]:
    if not seen[i]:
      top_sort_helper(G,i,seen,stack)

  stack.insert(0,v)

def is_DAG(G):  # {{{
    # Return true if G is a directed acyclic graph, and false otherwise.

    if topological_sort(G) == []:
        return False
    else:
        return True  # remove in your solution
# ----------------------------------------------------------------------------}}}


def findHamiltonian_DAG(G):  # {{{
    # If G is a DAG, then return a Hamiltonian path in G if it exists. This should
    # be a list of the vertices of G that form the path. If a path does not exist
    # or if G is not a DAG, then return None. The class AdjList has some new
    # methods that you might find useful.
    seen = [False for _ in G.nodes]
    explored = [False for _ in G.nodes]
    s = find_in_deg_zero(G)

    if s == None:
        return None

    seen[s] = True
    top_sort = [s]
    working_nodes = [s]
    while (len(working_nodes)) != 0:
        u = working_nodes.pop()
        if not explored[u]:
            explored[u] = True
            seen_any = False
        for v in G.adj[u]:
            if not explored[v]:
                working_nodes.append(v)
            if not seen[v]:
                seen_any = True
                top_sort.append(v)
                seen[v] = True
                explored[v] = True

        return top_sort


def randgraph_DAG(num_nodes):  # {{{
    # Generate a random DAG. Since bad_is_DAG calls bad_findCycle, this can be
    # *very* slow. Once you have implemented your is_DAG function, you might want
    # to change this.

    phi = (1 + 5**0.5)/2
    num_edges = int(num_nodes*phi)

    G = AdjList(num_nodes, directed=True)

    for _ in xrange(num_edges):
        new_edge = (randrange(num_nodes), randrange(num_nodes))
        G.add_edge(*new_edge)
    G.sort()

    if bad_is_DAG(G):
        return G
    return randgraph_DAG(num_nodes)
# ----------------------------------------------------------------------------}}}


def randgraph_DAGwithHam(num_nodes):  # {{{
    # Generate a random DAG with a Hamiltonian path. Since bad_is_DAG calls
    # bad_findCycle, this can be *very* slow. Once you have implemented your
    # is_DAG function, you might want to change this.

    phi = (1 + 5**0.5)/2
    num_edges = int(num_nodes*phi) - (num_nodes - 1)

    G = AdjList(num_nodes, directed=True)

    # choose a random path through the vertices and add those edges to G
    ham_path = next(islice(permutations(G.nodes, len(G)),
                           randrange(math.factorial(len(G))), None))
    for i in range(1, len(ham_path)):
        (prev_node, cur_node) = (ham_path[i-1], ham_path[i])
        G.add_edge(prev_node, cur_node)

    for _ in xrange(num_edges):
        new_edge = (randrange(num_nodes), randrange(num_nodes))
        G.add_edge(*new_edge)
    G.sort()

    if bad_is_DAG(G):
        return G
    return randgraph_DAGwithHam(num_nodes)
# ----------------------------------------------------------------------------}}}


# use this to check your topological_sort algorithm
A = randgraph_DAG(10)
S = topological_sort(A)
print A
print S


# use this to check your findHamiltonian_DAG algorithm
A = randgraph_DAGwithHam(10)
H = findHamiltonian_DAG(A)
print A
print H
if not A.is_path(H):
    print "whoops!"
