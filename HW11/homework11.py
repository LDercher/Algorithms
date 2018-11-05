# imports {{{1
from __future__ import division
from random import randrange
import math
from collections import Counter
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

def credit_card(L):
  recurse_lim = math.ceil(len(L)/4)
  cands = call(L,recurse_lim)
  return cands

def call(L,n): # {{{
  if len(L) <= n:
    return L
  cands = []
  mf = int(math.floor(len(L)/2))
  mc = int(math.ceil(len(L)/2))
  cands = (list(overHalf(L,mc)))
  A = call(L[:mc],n)
  B = call(L[mc:(len(L))],n)

  return cands

def overHalf(L, n):
  print "overhalf called"
  counter = Counter()
  cands = set()
  for i in L:
    counter[i] += 1
    if counter[i] >= n:
      if i not in cands:
        cands.add(i)

  return cands

#----------------------------------------------------------------------------}}}

# test your credit_card() solution using something like this
#for _ in xrange(10**4):
v = randrange(2,30)
s = randrange(2*v-1,v**2)
R = rand_cards(s,v)
A = ['a','b','a','d','e','f','a','a','a','b']
#B = [1,2,3,4,5,6,7,8,9,10]
print "CCa"
print A
print credit_card(A)
#print "CCb"
#credit_card(B)

