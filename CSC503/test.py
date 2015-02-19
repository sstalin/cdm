from lib.psim import PSim
 
comm = PSim(2)
source = 0

if comm.rank == source:
    #comm.send(1, "hello")
    print "I'm source and finished sending"
else:
    print "about to receive ..."
    comm.recv(0)
    #print m
    #comm.send(source, "Hi")
    #print comm.rank 

