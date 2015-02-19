from lib.psim import PSim
import random 

class Vertex(object):
    def __init__(self, id= None, edge_to= None, dist_to= None, solved= False):
        self.edge_to = edge_to
        self.dist_to = dist_to
        self.id = id

class Graph(object):
    def __init__(self, node_count):
        self.state = self.random_adj_matrix(node_count)

    def print_all_shortest(self, origin= 0):
        print "**************************************"
        print "Working with: "
        print self.state
        print "**************************************"
        vertices = self.p_single_shortest_path(origin= origin)
        result = ''
        for v in vertices:
            path = str(v.id)
            parent = v.edge_to
            while True:
                if parent is None:
                    break
                path = str(parent) + "-" + path
                next = vertices[parent]
                parent = next.edge_to
            result = result + "Path: " + path + ",  Dist to: " + str(v.dist_to) + "\n"  
        return result

        
    def random_adj_matrix(self, n):
        A = []
        for r in range(n):
            A.append([0]*n)
        for r in range(n):
            for c in range(0,r):
                A[r][c] = A[c][r]= random.randint(1, 10)
        return A
    
    def min_candidate(self, a, b):
        if a[1] < b[1]:
            return a
        else:
            return b
        
    def p_single_shortest_path(self, p=2, origin= 0, source= 0):
        n = len(self.state)
        solved = [None]*n
        next_solved = Vertex(id= origin, dist_to=0, solved=True)
        index = next_solved.id
        solved[index] = next_solved
        comm = PSim(p)
        local_vertices = comm.one2all_scatter(source, range(n))
        print "My rank:[ ", comm.rank , "] and my locals are : ", local_vertices
        while True:
            if None not in solved:
                break
            
            next_solved = comm.one2all_broadcast(source, next_solved)
            if next_solved not in solved:
                solved[next_solved.id] = next_solved
            #print "My rank:[ ", comm.rank, "] next solved id before the loop ", next_solved.id 
            message = None, float('inf'), None
            #begin local loop
            for i in local_vertices:
                # proceed only if i not solved
                if solved[i] is None:
                    #compute candidate distance for vertex
                    for j in xrange(n):
                        if i == j or solved[j] is None:
                            continue
                        next_dist = self.state[i][j] + solved[j].dist_to
                        if next_dist < message[1]:
                            message = i, next_dist, j
                                    
            #print "My rank:[", comm.rank, "] message before all2one_reduce:  ", message 
            next_candidate = comm.all2one_reduce(source, message, self.min_candidate)
            if comm.rank == source:
                #print "My rank[", comm.rank , "] and I see candidate ", next_candidate, "after reduce" 
                next_solved = Vertex(id= next_candidate[0]
                                     ,edge_to= next_candidate[2]
                                     ,dist_to= next_candidate[1], solved= True)

        return solved         


g = Graph(10)
out =  g.print_all_shortest(origin= 0)
print out

        
