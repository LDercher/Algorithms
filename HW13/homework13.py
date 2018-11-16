# imports {{{1
from __future__ import division
#---------------------------------------------------------------------------}}}1

def modified_rod_cut(P,n):  # {{{
  """ 
  - P is a table of prices. P[0] = 0, and P[k] = price for a rod of length k,
    where k > 0. 
  - n is the size of the rod to cut. By assumption n < len(P), so P[n] is
    defined. 
  - You should return a pair C, R. C is an array holding the sizes of the pieces
    you will cut the rod into, and R is the revenue that is associated with
    these cuts.
  """
  if n == 1:
    return [],0
  
  max_c = [n]
  max_rev = P[n]
  for k in range(1,n/2):
    L, PL = modified_rod_cut(P, k)
    R, PR = modified_rod_cut(P,k-l)
    PL -= 1
    PR -= 1
    if PL + PR > max_rev:
      max_rev = PL + PR
      max_c = list(set(L)|set(R))

  return max_c, max_rev
#----------------------------------------------------------------------------}}}
