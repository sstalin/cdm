from lib.psim import PSim

def parallel_add():
    A = [x for x in range(0,2346)]
    p = 2
    comm  = PSim(p)
    result = None
    
    if comm.rank == 1:
        half = A[len(A)/2:]
        print half
        comm.send(0, half)
        A = A[:len(A)/2]
        result = sum(A) + comm.recv(0)
    elif comm.rank == 0:
        A = comm.recv(1)
        comm.send(1, sum(A))
        #result = sum(A) + comm.recv(1)
    if comm.rank == 1:
        print "Parallel Result:%s" % result

parallel_add()
