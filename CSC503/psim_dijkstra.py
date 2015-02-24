from psim import PSim
import random, sys, re 

class Vertex(object):
    def __init__(self, id= None, edge_to= None, dist_to= None, solved= False):
        self.edge_to = edge_to
        self.dist_to = dist_to
        self.id = id

class Graph(object):
    def __init__(self, node_count= None, from_file= None):
        if node_count and not from_file:
            self.state = self.random_adj_matrix(node_count)
        if from_file and not node_count:
            self.state = self.read_from_file(from_file)
        self.solved_v = [None]*len(self.state)

    def read_from_file(self, fn):
        # open the file and get read to read data
        file = open(fn, "r");
        p = re.compile("\d+");

        # initialize the graph
        vertices, edges = map(int, p.findall(file.readline()))
        graph = [[None]*vertices for _ in range(vertices)]

        for i in range(edges):
            u, v, weight = map(int, p.findall(file.readline()))
            graph[u][v] = weight
            graph[v][u] = weight
        return graph
            
    def print_all_shortest(self):
        vertices = self.solved_v
        result = ''
        if None not in vertices:
            print "**************************************"
            print "Working with: "
            print self.state
            print "**************************************"
            for v in vertices:
                path = str(v.id)
                parent = v.edge_to
                while True:
                    if parent is None:
                        break
                    path = str(parent) + "-" + path
                    next = vertices[parent]
                    parent = next.edge_to
                result = result + "Path: " + path + ",  Cost: " + str(v.dist_to) + "\n"  
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

    #sequential single source shortes path        
    def s_SSP(self, origin= 0):
        n = len(self.state)
        solved = self.solved_v
        next_solved = Vertex(id= origin, dist_to=0, solved=True)
        solved[origin] = next_solved
        while None in solved:
            t = id, dist_to, parent = None, float('inf'), None
            #begin loop
            for i in xrange(n):
                # proceed only if i not solved
                if solved[i] is None:
                    #compute candidate distance for vertex
                    for j in xrange(n):
                        if i == j or solved[j] is None:
                            continue
                        if self.state[i][j] is None or self.state[i][j] is 0:
                            continue
                        next_dist = self.state[i][j] + solved[j].dist_to
                        if next_dist < t[1]:
                            t = id, dist_to, parent = i, next_dist, j
            next_solved = Vertex(id= id
                                 ,edge_to= parent
                                 ,dist_to= dist_to, solved= True)
            if next_solved not in solved:
                solved[id] = next_solved
        #set solved vertices
        self.solved_v = solved
                
    #parallel single source shortes path
    def p_SSP(self, p=2, origin= 0, source= 0):
        n = len(self.state)
        solved = [None]*n
        next_solved = Vertex(id= origin, dist_to=0, solved=True)
        solved[origin] = next_solved
        comm = PSim(p)
        local_vertices = comm.one2all_scatter(source, range(n))
        print "My rank:[ ", comm.rank , "] and my locals are : ", local_vertices
        while None in solved:
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
                        if self.state[i][j] is None or self.state[i][j] is 0:
                            continue
                        next_dist = self.state[i][j] + solved[j].dist_to
                        if next_dist < message[1]:
                            message = i, next_dist, j
                        
            next_candidate = comm.all2all_reduce(message, self.min_candidate)
            next_solved = Vertex(id= next_candidate[0]
                                     ,edge_to= next_candidate[2]
                                     ,dist_to= next_candidate[1], solved= True)
            if next_solved not in solved:
                solved[next_solved.id] = next_solved

        if comm.rank == source:
            self.solved_v = solved
            return solved
        else:
            return []


g = Graph(from_file = 'input.txt')
#g = Graph(node_count = 6)
#print "****************** SEQUENTIAL ******************"
#s = g.s_SSP(origin= 0)
#print  g.print_all_shortest()
print "****************** PARALLEL   ******************"
s = g.p_SSP(origin= 0)
print  g.print_all_shortest()

        
