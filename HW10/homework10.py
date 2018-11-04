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

# Base Case: Only one element 
    if (low == high): 
          return  A[low] 
    # Find the middle
    mid = (low + high) // 2
    # divide and conquer!!
    return max(MSP(A, low, mid), 
               MSP(A, mid + 1, high), 
               maxSum(A, low, mid, high))

def maxSum(arr, l, m, h) : 
      
    # Include elements on left of mid. 
    sum = 0; left_sum = -10000
      
    for i in range(m, l-1, -1) : 
        sum = sum + arr[i] 
          
        if (sum > left_sum) : 
            left_sum = sum 
      
      
    # Include elements on right of mid 
    sum = 0; right_sum = -1000
    for i in range(m + 1, h + 1) : 
        sum = sum + arr[i] 
          
        if (sum > right_sum) : 
            right_sum = sum 
      
  
    # Return sum of elements on left and right of mid 
    return left_sum + right_sum; 

#----------------------------------------------------------------------------}}}


# run this to test out your algorithm
for _ in range(1):
  A = rand_MSP(10, randrange(101))
  B = MSP_bad(A)
  G = MSP(A, 0, len(A)-1)
 # if not ( sum(A[G[0]:G[1]]) == G[2]):
  print "list to MSP on", A
   # print B
  print "MSP found", G
 #   break