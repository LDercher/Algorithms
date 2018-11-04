# imports {{{1
from __future__ import division
from random import randrange
import math
#---------------------------------------------------------------------------}}}1

def MSP_bad(A): # {{{
  sum_key = lambda x: x[2]
  S = [ (i, j, sum(A[i:j])) for i in range(len(A)) for j in range(i,len(A)+1) ]
  max_sum_triple = max(S, key=sum_key)

  return max_sum_triple
#----------------------------------------------------------------------------}}}
def rand_MSP(n, max_delta): # {{{
  max_delta_0 = max_delta // 2

  return [ randrange(-max_delta_0, max_delta_0+1) for _ in range(n) ]
#----------------------------------------------------------------------------}}}

def MSP(A, low, high):  # {{{
  # Find a sublist B = A[i:j] such that sum(B) is maximal. You should return the
  # triple (i, j, sum(B)). Note that i = j is allowed, in which case the sum is
  # 0.
  if A[low:high] == []:
    return (0, 0, [])

  half = int(math.ceil(low+ high / 2))

  left_ind = 0
  right_ind = 0

  max_sum = float('-inf')
  summation = 0
  for i in range(low, high):
    summation += A[i]
    if max(max_sum,summation) != max_sum: 
      max_sum = max(max_sum,summation)
      left_ind = i

  (i_lm, j_lm, l_lm) = MSP(A,low,half)
  (i_rm, j_rm, l_rm) = MSP(A,half,high)
  (i_l, j_l, l_l) = MSP(A,0,half)
  (i_r, j_r, l_r) = MSP(A,half,high)

  return 0,0,max((sum(l_lm),sum(l_rm),sum(l_l),sum(l_r)))






#----------------------------------------------------------------------------}}}


# run this to test out your algorithm
for _ in range(10**3):
  A = rand_MSP(randrange(1,51), randrange(101))
  B = MSP_bad(A)
  G = MSP(A, 0, len(A))
  if not ( sum(A[G[0]:G[1]]) == G[2] == B[2] ):
    print "whoops"
    print A
    print B
    print G
    break
