class Graph(object):
    def __init__(self):
        self.graph = {} # a dictionary mapping vertices to adjacent vertices
        self.marks = {} # marks both vertices and edges
        self.contractions = []
    def add_vertex(self, vertex, mark=False):
        if vertex in set(self.graph.keys()):
            raise KeyError('Vertex already exists in graph.')
        self.graph[vertex] = set([])
        self.marks[vertex] = mark
    def remove_vertex(self, v):
        incident_edges = [(v,u) for u in self.graph[v]] + [(u,v) for u in self.graph[v]]
        for marking in incident_edges:
            self.marks.pop(marking, None)
        self.marks.pop(v) # assert the KeyError here
        for neighbor in self.graph[v]:
            self.graph[neighbor].remove(v)
        self.graph.pop(v)
    def mark_vertex(self, vertex, mark=False):
        if vertex not in set(self.graph.keys()):
            raise KeyError('Vertex not in graph.')
        self.marks[vertex] = mark
    def add_edge(self, edge, mark=False): # not necessary for vertex to already exist
        v, u = edge
        try: self.graph[v].add(u)
        except KeyError: self.graph[v] = {u}
        try: self.graph[u].add(v)
        except KeyError: self.graph[u] = {v}
        self.marks[edge] = mark
    def add_edges(self, edge_set, mark=False):
        for edge in edge_set:
            self.add_edge(edge, mark)
    def remove_edge(self, edge):
        v,u = edge
        self.graph[v].remove(u)
        self.graph[u].remove(v)
        self.marks.pop[(v,u), None]
        self.marks.pop[(u,v), None]
    def get_neighbors(self, vertex):
        return self.graph[vertex]
    def mark_edge(self, edge, mark):
        if edge in set(self.marks.keys()): self.marks[edge] = mark
        elif edge[::-1] in set(self.marks.keys()): self.marks[edge[::-1]] = mark
        else: raise KeyError('Edge not in graph.')
    def get_unmarked_edge(self):
        for edge in self.marks.keys():
            if not self.marks[edge]:
                return edge
        return None
    def get_unmarked_edge(self, v): # returns a neighbor
        if not self.vertex_exists_in_graph(v):
            raise KeyError('Vertex does not exist in graph.')
        neighbors = self.graph[v]
        for u in neighbors:
            try:
                if not self.marks[(v,u)]:
                    return u
            except KeyError:
                if not self.marks[(u,v)]:
                    return u
        return None
    def vertex_exists_in_graph(self, vertex):
        try: self.graph[vertex]
        except KeyError: return False
        else: return True
    def edge_exists_in_graph(self, edge):
        try: self.marks[edge]
        except KeyError: return False
        else: return True
    def unmark_all(self):
        for edge_or_vertex in self.marks.keys():
            self.marks[edge_or_vertex] == False
    def get_vertices(self):
        return set(self.graph.keys())
    def contract_edge(self, edge, make_new=False):
        Exception('Graph:contract_edge is unimplented')
    def contract_blossom(self, blossom, make_new=False):
        # a blossom in an odd cycle s.t. there exists an M-alternating path for some matching M in G
        if make_new:
            G_prime = Graph()
            G_prime.graph = self.graph
            G_prime.marks = self.marks
            G_prime.contractions = self.contractions + [blossom]
            for edge in blossom:
                v,u = edge
                for neighbors in self.get_neighbors(v): G_prime.add_edge((blossom,v))
                for neighbors in self.get_neighbors(u): G_prime.add_edge((blossom,u))
            for edge in blossom:
                v,u = edge
                if G_prime.vertex_exists_in_graph(v): G_prime.remove_vertex(v)
                if G_prime.vertex_exists_in_graph(u): G_prime.remove_vertex(u)
            return G_prime
        else: Exception('contract_blossom with make_new=True is unimplemented.')

class Path(Graph):
    def __init__(self, edges=set([])):
        self.edges = edges
        self.vertices = set([x[0] for x in edges] + [x[1] for x in edges])
        if len(edges) == 0:
            self.end_1, self.end_2 = None, None
        else:
            counts = {}
            for v in self.vertices: counts[v] = 0
            for v,u in self.edges: counts[v] += 1; counts[u] += 1
            self.end_1, self.end_2 = [v for v in self.vertices if counts[v] == 1]
    def length(self):
        return len(self.edges)
    def get_ends(self):
        return (self.end_1, self.end_2)
    def add_edge(edge): # edges may still be invalid in this implementation
        v, u = edge
        if edge not in self.edges:
            self.edges.add(edge)
            self.vertices.add(v)
        else:
            raise ValueError('Edge already exists in path.')
        if len(self.edges) == 1: return
        elif v == self.end_1:
            if u == self.end_2: raise ValueError('Adding edge to path creates a cycle.')
            self.end_1 = u
        elif u == self.end_1:
            if v == self.end_2: raise ValueError('Adding edge to path creates a cycle.')
            self.end_1 = v
        elif v == self.end_2:
            if u == self.end_1: raise ValueError('Adding edge to path creates a cycle.')
            self.end_2 = u
        elif u == self.end_2:
            if v == self.end_1: raise ValueError('Adding edge to path creates a cycle.')
            self.end_2 = v

class Matching(object):
    def __init__(self, init_matches=set([])):
        self.edges = init_matches
        self.marks, self.matches = {}, {}
        for match in init_matches:
            v,u = match
            self.matches[v] = u; self.matches[u] = v
            self.marks[match] = False
    def length(self):
        return len(self.edges)
    def add_edge(self, edge, mark=False):
        if edge in self.edges():
            raise ValueError('Match already exists in matching.')
        v, u = edge
        self.edges.add(edge)
        self.matches[v] = u
        self.matches[u] = v
        self.marks[edge] = mark
    def remove_match(self, edge):
        if not self.edge_in_matching(edge):
            raise KeyError('Edge does not exist in matching.')
        self.edges -= {edge,edge[::-1]}
        try: self.marks.pop(edge)
        except KeyError: self.marks(edge[::-1])
        self.matches.pop(edge[0]); self.matches.pop(edge[1])
    def get_matched_vertex(self, vertex, raise_error=True):
        try:
            return self.matches[vertex]
        except KeyError:
            if raise_error:
                raise KeyError('Vertex is unmatched.')
            return None
    def get_matched_edge(self, vertex, raise_error=True):
        try:
            return (vertex,self.matches[vertex])
        except KeyError:
            if raise_error:
                raise KeyError('Vertex is unmatched.')
            return None
    def edge_in_matching(self, e):
        return e in self.edges or e[::-1] in self.edges
    def augment(self, aug_path):
        return Matching((self.edges - aug_path.edges) | (aug_path.edges - self.edges))
    def mark_all(self):
        for edge in self.marks.keys():
            self.marks[edge] = True
    def covered_vertices(self):
        return set(self.matches.keys())
    def contract_blossom(self, edges, make_new=False):
        if make_new:
            M_prime = Matching()
            M_prime.edges = self.edges
            M_prime.matches = self.matches
            M_prime.marks = self.marks
            blossom_vertices = set([e[0] for e in edges] + [e[1] for e in edges])

            # finding the base of the blossom, should be unmatched
            for v in blossom_vertices:
                if M.get_matched_vertex(v, raise_error=False) is None:
                    blossom_base = v; break

            # remove the matches within the blossom
            for v in blossom_vertices - {blossom_base}:
                match = M.get_matched_edge(v)
                M_prime.remove_match(match)

            # DEBUGGING: this should error out (tries to update match of the
            # blossom base, which should not exist)
            stem_tip = M_prime.get_matched_vertex(blossom_base)
            M_prime.edges -= {(stem_tip,blossom_base),(blossom_base,stem_tip)}
            M_prime.edges.add((stem_tip,blossom))
            try:
                stem_tip_mark = M_prime.marks[(stem_tip,blossom_base)]
                M_prime.marks.pop((stem_tip,blossom_base))
            except KeyError:
                stem_tip_mark = M_prime.marks[(blossom_base,stem_tip)]
                M_prime.marks.pop((blossom_base,stem_tip))
            M_prime.marks[(stem_tip,blossom)] = root_tip_mark
            M_prime.matches[stem_tip] = blossom
            M_prime.matches[blossom] = stem_tip
            M_prime.matches.pop(blossom_base)
            return M_prime
        else:
            raise Exception('Matching:contract unimplemented with make_new=False')

class Tree(Graph):
    def __init__(self, root):
        super(Tree, self).__init__()
        self.root = root
        self.add_vertex(root)
        self.parents = { self.root: None }
    def add_edge(self, edge):
        v, u = edge
        super(Tree, self).add_edge(edge)
        if v in self.get_vertices(): self.parents[u] = v
        elif u in self.get_vertices(): self.parents[v] = u
        else: raise KeyError('Adding edge to tree violates connectedness of graph')
    # i dont think I need this function, and can just call super.
    def get_unmarked_vertex(self):
        for vertex in self.graph.keys():
            if not self.marks[vertex] and self.elevation(vertex) % 2 == 0:
                return vertex
        return None
    def root_path(self, vertex):
        path_edges = []
        while True:
            parent = self.parents[vertex]
            if parent is None:
                return set(path_edges)
            path_edges.append((vertex,path))
            vertex = parent
    def elevation(self, vertex):
        return len(self.root_path(vertex))
    def get_path(self, v, w):
        v_path = self.root_path(v)
        w_path = self.root_path(w)
        return (v_path | w_path) - (v_path & w_path)

class Forest(object):
    def __init__(self):
        self.trees = set([])
    def plant(self, tree):
        self.trees.add(tree)
    def get_unmarked_vertex(self):
        for tree in self.trees:
            vertex = tree.get_unmarked_vertex()
            if vertex is not None:
                return (vertex, tree)
        return (None, None)
    def get_tree(self, vertex):
        for tree in self.trees:
            if vertex in tree.get_vertices():
                return tree
        return None
