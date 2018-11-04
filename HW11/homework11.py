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
  print L
  if len(L) == 1:
    return None


  if len(L) % 2 == 0:
    m = int(len(L)/2)
    credit_card(L[:m])
    credit_card(L[m:(len(L))])
  else:
    mf = int(math.floor(len(L)/2))
    mc = int(math.ceil(len(L)/2))
   # print "mf =", mf, " mc = ", mc, " of ", len(L)
    credit_card(L[:mc])
    credit_card(L[mc:(len(L))])


#----------------------------------------------------------------------------}}}

# test your credit_card() solution using something like this
#for _ in xrange(10**4):
v = randrange(2,30)
s = randrange(2*v-1,v**2)
R = rand_cards(s,v)
A = [1,2,3,4,5,6,7,8,9]
B = [1,2,3,4,5,6,7,8,9,10]

credit_card(A)
credit_card(B)

