# imports {{{1
from __future__ import division
from random import randrange
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

  if low == high:
    return A[0]

  half = (low + high)/2
  right_ind = 0
  right_ind = 0
  left_msl = MSP(A,0,half)
  right_msl = MSP(A,half, len(A)-1)
  left_sum = float('-inf')
  right_sum = float('-inf')
  summation = 0
  for i in range(half, high):
    summation += A[i]
    if max(left_sum,summation) != left_sum: 
      left_sum = max(left_sum,summation)
      left_ind = i
  
  summation = 0
  for i in range(low,half):
    summation += A[i]
    if max(right_sum,summation) != right_sum: 
      right_sum = max(right_sum,summation)
      right_ind = i

  ans = max(left_sum,right_sum)
  
  return right_ind, left_ind, max(ans, left_sum + right_sum)

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
