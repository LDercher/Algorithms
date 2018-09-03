# imports {{{1
from __future__ import division
import math
import pdb
from random import randrange
#---------------------------------------------------------------------------}}}1

class Heap: # {{{1
  # A heap data structure. A node n in the tree is a pair n = (k,v), where k is
  # the key of n and v is the value. The tree is always balanced, and is stored
  # in a flat list, Heap.nodes.
  #
  # if Heap.nodes = [a, b, c, d, e, f, g, h, i, j, k, l, m, n], then this
  # corresponds to the tree
  #          ____a____
  #         /         \
  #       _b_         _c_
  #      /   \       /   \
  #     d     e     f     g
  #    / \   / \   / \   /
  #   h   i j   k l   m n
  #
  # The functions below are mostly self-explanatory. If H is a heap, then:
  #   H.__getitem__(index) is run to return H[index],
  #   H.__delitem__(index) is run to execute del H[index],
  #   H.__len__ is run to execute len(H)
  #   H.__str__ is run to execute str(H), print H, etc.

  def __init__(self, initial = []): # {{{
    self.nodes = []
    for n in initial:
      self.add(n)
  #--------------------------------------------------------------------------}}}

  def _key(self, index):  # {{{
    return self.nodes[index][0]
  #--------------------------------------------------------------------------}}}

  def _parent_index(self, index): # {{{
    # Return the index of the parent of the node at given index. In the example
    # above, the index of node f is 5, so Heap._parent_index(5) = 2, the index
    # of the node c.

    return None if index <= 0 else int(math.floor(index /2))
  #--------------------------------------------------------------------------}}}
  def _parent(self, index): # {{{
    # Return the parent of the node at the given index. In the example above,
    # the index of node f is 5, so Heap._parent(5) = c. Return the special
    # python value of None if there is no parent.

    # if no parent
    return None if index <= 0 else self.nodes[self._parent_index(index)][1]
  #--------------------------------------------------------------------------}}}
  def _parent_key(self, index): # {{{
    # Return the parent of the node at the given index. In the example above,
    # the index of node f is 5, so Heap._parent_key(5) = 3. Return the special
    # python value of None if there is no parent.

    # if no parent
    return None if index <= 0 else ord(self.nodes[self._parent_index(index)][1] - 66)

  def swap(self, ind1, ind2):
    if (ind1 >= 0) and (ind2 >= 0):
      temp_node = self.nodes[ind1]
      self.nodes[ind1] = self.nodes[ind2]
      self.nodes[ind2] = temp_node




  #--------------------------------------------------------------------------}}}
  def _heapify_up(self, index): # {{{
    # heapify_up, as discussed in class and the the book.
   # if index > 0:
    #  parent_ind = self._parent_index(index)
    #  if self._key(index) < self._key(parent_ind):
     #   self.swap(index,parent_ind)
    #    self._heapify_up(parent_ind)
    #pdb.set_trace()
    if index == 0:
      print "no swapping done on ", self.nodes
      return
    parent_ind = self._parent_index(index)
    print "parent index at " ,index, " found to be ", parent_ind
    while self._key(parent_ind) > self._key(index):
      print "parent key = ", self._key(parent_ind), "surr key = ", self._key(index)
      print "swappoing at index ", index, " and ", parent_ind, " on ", self.nodes
      self.swap(index,parent_ind)
      index = parent_ind
      parent_ind = self._parent_index(index)
      print "after swap ", self.nodes
      if self._parent(index) == None:
        print "parent index at ", index, " found to be null"
        break
      

  #---------------------------------------------------------------------------}}}
  def add(self, new_node):  # {{{
    # new_node is a tuple, new_node=(key,value)
    print "adding new node (", new_node[0], ", ", new_node[1], ")"
    self.nodes.append(new_node)
    print "heapifying from index", len(self.nodes) - 1
    self._heapify_up(len(self.nodes)-1)
  #--------------------------------------------------------------------------}}}

  def _child_index(self, index, direct):  # {{{
    return 2*index + 1 + direct
  #---------------------------------------------------------------------------}}}
  def _child(self, index, direct): # {{{
    child_index = self._child_index(index, direct)
    if child_index >= len(self.nodes):
      return None
    return self.nodes[child_index]
  #---------------------------------------------------------------------------}}}
  def _child_key(self, index, direct): # {{{
    child_index = self._child_index(index, direct)
    if child_index >= len(self.nodes):
      return None
    return self._key(child_index)
  #---------------------------------------------------------------------------}}}
  def _heapify_down(self, index): # {{{
    bottom_level = self._level(len(self.nodes)-1)
    while self._level(index) < bottom_level:
      children_keys = [ self._child_key(index, d) for d in [0,1] ]
      children_keys = [ c for c in children_keys if c != None ]
      if children_keys == [] or self._key(index) <= min(children_keys):
        break
      if children_keys[0] <= children_keys[-1]:
        min_child_index = self._child_index(index,0)
      else:
        min_child_index = self._child_index(index,1)
      swap = self.nodes[min_child_index]
      self.nodes[min_child_index] = self.nodes[index]
      self.nodes[index] = swap
      index = min_child_index
  #---------------------------------------------------------------------------}}}
  def _level(self,index): # {{{
    return int( math.floor( math.log(index+1) ) )
  #----------------------------------------------------------------------------}}}
  def remove(self, index):  # {{{
    self.nodes[index] = self.nodes[-1]
    del self.nodes[-1]
    self._heapify_down(index)
  #--------------------------------------------------------------------------}}}

  def __getitem__(self, index):  # {{{
    return self.nodes[index]
  #--------------------------------------------------------------------------}}}
  def __delitem__(self, index):  # {{{
    self.remove(index)
  #--------------------------------------------------------------------------}}}
  def __len__(self):  # {{{
    return len(self.nodes)
  #--------------------------------------------------------------------------}}}
  def __str__(self):  # {{{
    return str(self.nodes)
  #--------------------------------------------------------------------------}}}
#----------------------------------------------------------------------------}}}1

class PQ: # {{{1
  def __init__(self, initial = []): # {{{
    self.elements = Heap(initial=initial)
  #--------------------------------------------------------------------------}}}

  def add(self, new_node):  # {{{
    # Add new_node to the priority queue. The argument new_node is a tuple,
    # new_node=(key,value)

    return  # remove in your solution
  #--------------------------------------------------------------------------}}}

  def pop(self): # {{{
    # Return the *value* (not the key) of the top of the priority queue. If the
    # top is (k,v), it should return v. Raise an exception if the queue is
    # empty.

    # if the queue is empty
    raise IndexError
  #--------------------------------------------------------------------------}}}

  def __len__(self):  # {{{
    return len(self.hashes)
  #--------------------------------------------------------------------------}}}
  def __str__(self):  # {{{
    return str(self.nodes)
  #--------------------------------------------------------------------------}}}
#----------------------------------------------------------------------------}}}1

I = [ (2,"b"),
      (15,"c"),
      (16,"d"),
      (1,"a"),
      (17,"e"),
      (8,"f"),
      (20,"g"),
      (15,"h"),
      (10,"i"),
      (3,"j"),
      (7,"k"),
      (11,"l")]

J = [ (45,"b"),
      (15,"c"),
      (16,"d"),
      (345,"a"),
      (17,"e"),
      (1,"f"),
      (20,"g"),
      (15,"h"),
      (14,"i"),
      (36,"j"),
      (47,"k"),
      (11,"l")]
H = Heap(initial=J)
print "First run:"
print H

# This should print 
# First run:
# [(1, 'a'), (2, 'b'), (8, 'f'), (10, 'i'), (3, 'j'), (11, 'l'), (20, 'g'), (15, 'h'), (15, 'c'), (17, 'e'), (7, 'k'), (16, 'd')]


H.add((1,"m"))
H.add((100,"n"))
H.add((5,"o"))
print "Second run:"
print H

# This should print
# Second run:
# [(1, 'a'), (2, 'b'), (1, 'm'), (10, 'i'), (3, 'j'), (8, 'f'), (5, 'o'), (15, 'h'), (15, 'c'), (17, 'e'), (7, 'k'), (16, 'd'), (11, 'l'), (100, 'n'), (20, 'g')]


def sort_with_PQ(L):  # {{{
  # Input is a list L. Return the sorted list. The sort should be linear in the
  # PQ operations. That is, it should run in O(n*O(PQ)).

  return  # remove in your solution
#----------------------------------------------------------------------------}}}

# you can test your sort_with_PQ function like this:
R = [ randrange(20) for _ in range(15) ]
print R
print sort_with_PQ(R)
