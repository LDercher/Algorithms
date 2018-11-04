# imports {{{1
from __future__ import division
from random import randrange
import math
#---------------------------------------------------------------------------}}}1

def rand_perm(size):  # {{{
  p = []
  while len(p) < size:
    r = randrange(size)
    if r not in p:
      p.append(r)
  return p
#----------------------------------------------------------------------------}}}
def rand_cards(n, max_value=2):  # {{{
  base = []
  for value in range(1,max_value):
    max_reps = n//2 - len(base) - 1 + (n % 2)
    if max_reps == 0:
      break
    base += [value]*randrange(1,max_reps+1)
  base += [max_value]*(n-len(base))

  perm = rand_perm(n)
  base_perm = [ base[perm[i]] for i in range(n) ]

  return base_perm
#----------------------------------------------------------------------------}}}

def credit_card(L): # {{{
  # Detect whether there is an element of L that occurs more than half the time.
  # You should return the element if there is one as well as a count of the
  # number of times it occurs in L. If there is no such element, return None, 0.



  return find_majority_elem(L,len(L))[0]  # if there is no majority element

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def find_majority_elem(L,n):

  if n <= 2:
    return L
    
  candidates = union(find_majority_elem(L[:int(math.floor(n/2))],int(math.floor(n/2))),find_majority_elem(L[:int(math.ceil(n/2))],int(math.ceil(n/2))))

  print "length of candidates ",len(candidates), "length of L", len(L) 

  majority = []
  for i in range(len(candidates)):
    count = 0
    j = 1
    while j < n:
      k = L[j]
      l = candidates[i]
      if L[j] == candidates[i]:
        count +=1
      j +=1

    if count >= math.ceil(n/2):
      majority.append((candidates[i],count))

    return majority
#----------------------------------------------------------------------------}}}

# test your credit_card() solution using something like this
for _ in xrange(10**4):
  v = randrange(2,30)
  s = randrange(2*v-1,v**2)
  R = rand_cards(s,v)
  A, count = credit_card(R)
  if A != v:
    print "whoops"
    print R
    print A
    break
