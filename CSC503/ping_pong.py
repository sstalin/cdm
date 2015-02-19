from lib.psim import PSim

p = 4
comm = PSim(4)
source = 0

if comm.rank == source:
    print comm.recv(1) + "Pong"

left = int(comm.rank) - 1 
right = int(comm.rank) + 1

if comm.rank % 2 == 0 and comm.rank > source:
    message = comm.recv(right) +  "Pong"
    comm.send(left, message)
    #print comm.rank, "I'm even, my message", message

elif comm.rank % 2 > 0:
    if comm.rank == p-1:
        message = "Ping"
    else:    
        message = comm.recv(right) + "Ping"
    comm.send(left, message)
    #print comm.rank, "I'm odd , my message; ", message

