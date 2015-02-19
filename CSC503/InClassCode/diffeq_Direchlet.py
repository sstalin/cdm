from psim import PSim
from nlib import *
from random import random

import sys

# input domain
a = 0.0 # time zero
b = 1.0 # rime 1 second
# input Dirichelet boundary conditions
fa = 0.0 # meters
fb = 1.0 # 1 meter after b=1 seconds

#input physical parameter
alpha = 5.0 # g/mass/2

# simulation parameters
p = int(sys.argv[1])
n = int(sys.argv[2])
h = (b-a)/n


def rules(Aip,Ai,Aim):
    return (Aip+Aim)/2.0 + alpha*h*h


def evolve(A):
    n = len(A)
    B = [0 for k in range(n)]
    for i in range(1,n-1):
        B[i] = rules(A[i-1],A[i],A[i+1])
    return B

def plot(B):
    points =  [(a+i*h, xi) for i,xi in enumerate(B[0])]
    canvas.plot(points).save('trajectory.png')

def parallel_print(comm,A):
    B = A[1:-1]
    B = comm.all2one_collect(0,B)
    if comm.rank == 0:        
        print B
        plot(B)

comm = PSim(p)
root = 0
if comm.rank == root:
    canvas = Canvas()
    #A = [choice([0,1]) for k in range(n)]
    A = [random() for k in range(n)]
    print A
else:
    A = None

A = comm.one2all_scatter(root,A)
A = [0]+A+[0]
right = (comm.rank + 1) % comm.nprocs
left = (comm.rank - 1 + comm.nprocs) % comm.nprocs

for t in range(200):
    comm.send(right, A[-2])
    A[0] = comm.recv(left)
    comm.send(left, A[1])
    A[-1] = comm.recv(right)    

    A = evolve(A)
    if comm.rank == 0:
        A[1] = fa
    if comm.rank == p-1:
        A[-2] = fb

    if t%10 == 0:
        parallel_print(comm,A)
    t += 1
