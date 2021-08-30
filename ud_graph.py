# Course: 261
# Author: Eric Pauls
# Assignment: 6
# Description: implementation of an undirected graph


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        if u not in self.adj_list:
            self.adj_list[u] = [v]
        if v not in self.adj_list:
            self.adj_list[v] = [u]
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)


    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if v not in self.adj_list or u not in self.adj_list:
            return
        if v in self.adj_list[u]:
            self.adj_list[u].remove(v)
        if u in self.adj_list[v]:
            self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list:
            return
        for vertex in self.adj_list:
            if v in self.adj_list[vertex]:
                self.adj_list[vertex].remove(v)
        del self.adj_list[v]
        

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vert_list = []
        for vert in self.adj_list:
            vert_list.append(vert)
        return vert_list
       

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges = []
        for vert in self.adj_list:
            for edge in self.adj_list[vert]:
                if (edge, vert) not in edges:
                    edges.append((vert, edge))
        return edges
        

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if len(path) == 1:         # if the length is only 1
            if path[0] not in self.adj_list:
                return False
            else:
                return True
        edges = self.get_edges()        # create list of edges
        for vert in range(len(path) - 1):   # for each vertex in path, check if there is a connecting edge
            if vert is not path[len(path) - 1]:
                if (path[vert], path[vert + 1]) not in edges and (path[vert + 1], path[vert]) not in edges:
                    return False
        return True

    def dfs_helper(self, v_end, output, stack):
        """recursive helper for dfs"""
        if len(stack) > 0:      # if the stack is empty, return the output
            v = stack.pop()
            if v not in output:
                output.append(v)    # add element popped from the stack to output
                if v == v_end:
                    return output
                temp = []       # crete a temporary list to be sorted and added to the stack
                for element in self.adj_list[v]:
                    temp.append(element)
                temp.sort(reverse=True)  # add the vertices to the stack so they are processed in lexicographical order
                for vertex in temp:
                    stack.append(vertex)
            return self.dfs_helper(v_end, output, stack)
        return output


    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        output = []
        stack = [v_start]   # add start to the stack
        if v_start not in self.adj_list:
            return output
        return self.dfs_helper(v_end, output, stack)    # call recursive helper


    def bfs_helper(self, v_end, visited, queue):
        """recursive helper for bfs"""
        if len(queue) > 0:      # return visited if the queue is empty
            v = queue.pop(0)    # dequeue
            if v not in visited:
                visited.append(v)   # add v to visited if v is not already in there
                if v is v_end:
                    return visited
                temp = []       # create temp list to help add to queue in lexicographical order
                for element in self.adj_list[v]:
                    temp.append(element)
                temp.sort()
                for vertex in temp:
                    queue.append(vertex)    # add all vertices to the queue in lexicographical order
            return self.bfs_helper(v_end, visited, queue)
        return visited
        

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        visited = []
        queue = [v_start]
        if v_start not in self.adj_list:
            return visited
        return self.bfs_helper(v_end, visited, queue)   # call recursive helper
        
        

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        tracker = {}
        for v in self.adj_list:
            tracker[v] = False  # create a tracker to track visited vertices, set all values to false
        components = 0
        for v in tracker:
            if tracker[v] is False:    # if vertex has not been visited
                output = self.dfs(v)    # call dfs to get all connected vertices to v
                for v in output:
                    tracker[v] = True   # set to true to indicate vertex has been visited
                components += 1     # increment components count
        return components


    def cycle_helper(self, v, tracker, parent=None):
        """recursive helper for has cycle method"""
        tracker[v] = True       # set true for the node we are visiting
        for vertices in self.adj_list[v]:   # for all vertices adjacent to v
            if tracker[vertices] is False:  # if vertex has not been visited
                if self.cycle_helper(vertices, tracker, v) is True:    # if cycle helper for adj vertex is true
                    return True    # retrun true
            elif parent != vertices:
                return True
        return False



    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        if len(self.adj_list) < 3:
            return False    # return false if graph is too small for a cycle
        tracker = {}
        for v in self.adj_list:
            tracker[v] = False  # create a visited tracker
        for v in self.adj_list:
            if tracker[v] is False:
                if self.cycle_helper(v, tracker) is True:   # call recursive helper
                    return True
        return False


   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
