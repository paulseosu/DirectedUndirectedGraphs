# Course: CS261 - Data Structures
# Author: Eric Pauls
# Assignment: 6
# Description: implementation of a directed graph. First 50 lines are skeleton code provided to me in the assignment.
# the rest has been coded by me.

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        adds a vertex to the directed graph
        """
        v = []
        self.adj_matrix.append(v)
        for vertex in self.adj_matrix:
            vertex.append(0)
        for vertex in range(self.v_count):
            v.append(0)
        self.v_count += 1
        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        adds an edge between vertices in a directed graph
        """
        if weight < 1:
            return
        if src == dst:
            return
        if src not in range(self.v_count) or dst not in range(self.v_count):
            return
        self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        removes an edge from the directed graph
        """
        if src not in range(self.v_count) or dst not in range(self.v_count):
            return
        self.adj_matrix[src][dst] = 0


    def get_vertices(self) -> []:
        """
        returns all the vertices in the graph
        """
        all = []
        start = 0
        for v in self.adj_matrix:
            all.append(start)
            start += 1
        return all

    def get_edges(self) -> []:
        """
        returns all the edges in the graph
        """
        all = []
        src = 0
        for v in self.adj_matrix:
            dst = 0
            for e in v:
                if e > 0:
                    all.append((src, dst, e))
                dst += 1
            src += 1
        return all

    def is_valid_path(self, path: []) -> bool:
        """
        checks if given path is valid
        """
        index = 1
        for v in path:
            if v is not path[-1]:
                if self.adj_matrix[v][path[index]] is None:
                    return False
                if self.adj_matrix[v][path[index]] < 1:
                    return False
                index += 1
        return True

    def dfs_helper(self, v_end, output, stack):
        """recursive helper for bfs"""
        if len(stack) > 0:      # if the stack is empty, return the output
            v = stack.pop()
            if v not in output:
                output.append(v)    # add element popped from the stack to output
                if v == v_end:
                    return output
                temp = []       # crete a temporary list to be sorted and added to the stack
                for element in range(0, len(self.adj_matrix[v])):
                    if self.adj_matrix[v][element] != 0:
                        temp.append(element)
                temp.sort(reverse=True)  # add the vertices to the stack so they are processed in lexicographical order
                for vertex in temp:
                    stack.append(vertex)
            return self.dfs_helper(v_end, output, stack)
        return output

    def dfs(self, v_start, v_end=None) -> []:
        """
        depth first search for a directed graph
        """
        output = []
        stack = [v_start]  # add start to the stack
        if v_start not in range(self.v_count):
            return output
        return self.dfs_helper(v_end, output, stack)  # call recursive helper

    def bfs_helper(self, v_end, visited, queue):
        """recursive helper for bfs"""
        if len(queue) > 0:  # return visited if the queue is empty
            v = queue.pop(0)  # dequeue
            if v not in visited:
                visited.append(v)  # add v to visited if v is not already in there
                if v is v_end:
                    return visited
                temp = []  # create temp list to help add to queue in lexicographical order
                for element in range(0, len(self.adj_matrix[v])):
                    if self.adj_matrix[v][element] != 0:
                        temp.append(element)
                temp.sort()
                for vertex in temp:
                    queue.append(vertex)  # add all vertices to the queue in lexicographical order
            return self.bfs_helper(v_end, visited, queue)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        """
        visited = []
        queue = [v_start]
        if v_start not in range(self.v_count):
            return visited
        return self.bfs_helper(v_end, visited, queue)  # call recursive helper

    def cycle_helper(self, v, tracker1, tracker2):
        """recursive helper for has cycle method"""
        tracker1[v] = True       # set true for the node we are visiting
        tracker2[v] = True
        for vertices in range(len(self.adj_matrix[v])):   # for all vertices adjacent to v
            if self.adj_matrix[v][vertices] != 0:    # if there is a connection between vertices
                if tracker1[vertices] is False:  # if vertex has not been visited
                    if self.cycle_helper(vertices, tracker1, tracker2) is True:    # if cycle helper for adj vertex is true
                        return True    # return true
                elif tracker2[vertices] is True:
                    return True
        tracker2[v] = False
        return False


    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        if len(self.adj_matrix) < 3:
            return False    # return false if graph is too small for a cycle
        tracker1 = {}
        tracker2 = {}
        for v in range(self.v_count):
            tracker1[v] = False  # create a visited tracker1
        for v in range(self.v_count):
            tracker2[v] = False  # create a tracker2 for recursion
        for v in range(self.v_count):
            if tracker1[v] is False:
                if self.cycle_helper(v, tracker1, tracker2) is True:   # call recursive helper
                    return True
        return False


    def dijkstra_helper(self, visited, priority_queue):
        """helper function for dijkstra's algorithm"""
        while len(priority_queue) > 0:      # while priority queue isnt empty
            temp = priority_queue.pop(0)
            v = temp[0]     # key is vertex v
            d = temp[1]     # value is min distance d to vertex d
            if visited[v] == float('inf'):     # if v is not in the map of visited vertices
                visited[v] = d      # value = d
                for v_i in range(len(self.adj_matrix[v])): # for each successor vi of v
                    if self.adj_matrix[v][v_i] > 0:
                        d_i = self.adj_matrix[v][v_i]   # let di be the cost/distance associated with edge (v, vi)
                        insert = [v_i, d + d_i]        # insert vi into priority queue with distance d + di
                        if len(priority_queue) == 0:
                            priority_queue.append(insert) # if priority queue is empty, insert at index 0
                        else:
                            index = 0
                            while insert not in priority_queue:   # while vi is not in priority queue
                                if priority_queue[index][1] > insert[1]:    # if index value > insert value (vi)
                                    priority_queue.insert(index, insert)    # insert vi into priority queue
                                elif index == len(priority_queue) - 1:  # if end of que is reached
                                    priority_queue.append(insert)   # insert vi into the end of the queue
                                index += 1     # increment the index we are checking
        return visited


    def dijkstra(self, src: int) -> []:
        """
        implementation of Dijkstra's algorithm
        """
        visited = {}    # track vertices already visited
        for v in range(self.v_count):
            visited[v] = float('inf')       # distance for all in visited are initialized to infinity
        priority_queue = []
        priority_queue.append([src, 0])     # add start to the priority queue
        visited = self.dijkstra_helper(visited, priority_queue)    # visited is dijkstra output
        output = []
        for key in visited:
            output.append(visited[key])     # create list for output
        return output

# Below is a series of tests showing that each method works properly

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
