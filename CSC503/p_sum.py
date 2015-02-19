from lib.psim import *
import sys
import random

p = 4

source = 0
# make random array
A = [random.randint(1,100) for i in range(10)]
#print A 
#print sum(A)
comm = PSim(p)

#computes sum of array elements
def sum(A):
    result = 0
    for i in A:
        result= result + i
    return result

a = comm.one2all_scatter(source, A)
a_sum = sum(a)
print "My rank is:", comm.rank, "and my sum is:", a_sum 

w = comm.all2one_collect(0, a_sum)

if comm.rank == source:
   print "I'm the source and received ", w
   sum = reduce(lambda x,y: x+y, w)
   print "Final sum is ", sum
   
