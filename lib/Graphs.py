import copy

class Graph(object):
    def __init__(self):
        self.graph = {} # a dictionary mapping vertices to adjacent vertices
        self.marks = {} # marks both vertices and edges
    def add_vertex(self, vertex, mark=False):
        if vertex in set(self.graph.keys()):
            raise KeyError('Vertex already exists in graph.')
        self.graph[vertex] = set([])
        self.marks[vertex] = mark
    def remove_vertex(self, v):
        incident_edges = [(v,u) for u in self.graph[v]]
        for marking in incident_edges:
            try: self.marks.pop(marking)
            except KeyError: self.marks.pop(marking[::-1])
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
        self.marks[v] = mark
        self.marks[u] = mark
    def add_edges(self, edge_set, mark=False):
        for edge in edge_set:
            self.add_edge(edge, mark)
    def remove_edge(self, edge):
        v,u = edge
        self.graph[v].pop(u)
        self.graph[u].pop(v)
        try: self.marks.pop((v,u))
        except KeyError: self.marks.pop((u,v))
    def get_neighbors(self, vertex):
        return self.graph[vertex]
    def mark_edge(self, edge, mark):
        if edge in set(self.marks.keys()): self.marks[edge] = mark
        elif edge[::-1] in set(self.marks.keys()): self.marks[edge[::-1]] = mark
        else: raise KeyError('Edge not in graph.')
    def get_unmarked_edge(self):
        for edge in set([e for e in self.marks.keys() if len(e) == 2]):
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
    def edge_exists_in_graph(self, e):
        edges = set(self.marks.keys())
        return e in edges or e[::-1] in edges
    def unmark_all(self):
        for edge_or_vertex in self.marks.keys():
            self.marks[edge_or_vertex] == False
    def get_vertices(self):
        return set(self.graph.keys())
    def contract_edge(self, edge, make_new=False):
        raise Exception('Graph:contract_edge is unimplented')

    '''
    This can be an issue: The base might actually be unmatched to some preceding vertex.
    '''
    def contract_blossom(self, blossom, make_new=False): # this isn't handling nested blossoms
        # a blossom in an odd cycle s.t. there exists an M-alternating path for some matching M in G
        blossom_vertices = set([e[0] for e in blossom] + [e[1] for e in blossom])
        if make_new:
            G_prime = copy.deepcopy(self)
            G_prime.add_vertex(blossom)
            for v in blossom_vertices:
                for external_neighbor in self.get_neighbors(v)-blossom_vertices:
                    G_prime.add_edge((blossom,external_neighbor))
                G_prime.remove_vertex(v)
            return G_prime
        else:
            raise Exception('Graph:contract_blossom with make_new=True is unimplemented.')

class Path(Graph):
    def __init__(self, edges=set([])):
        super(Path, self).__init__()
        self.edges, self.vertices = set([]), set([])
        for edge in edges: self.add_edge(edge, raise_error=False)
        if len(edges) != 0:
            self.ends = tuple([v for v in self.vertices if len(self.graph[v]) == 1])
        else:
            self.ends = (None, None)
        if len(self.ends) != 2:
            raise Exception('Initalizing edge set does not form a path.')
    def get_edges(self): return self.edges
    def get_length(self): return len(self.edges)
    def get_ends(self): return self.ends
    def add_edge(self, edge, raise_error=True):
        if raise_error:
            if self.edge_exists_in_graph(edge):
                raise ValueError('Edge already exists in graph.')
        v, u = edge
        self.edges.add(edge)
        self.vertices |= {v,u}
        super(Path, self).add_edge(edge)
        self.ends = tuple([v for v in self.vertices if len(self.graph[v]) == 1])
        if raise_error:
            if len(self.ends) != 2:
                raise Exception('Adding edge to path yields a non-path.')
    def add_edges(self, edge_set):
        for edge in edge_set:
            self.add_edge(edge, raise_error=False)

class Matching(object):
    # TODO: POTENTIAL ERROR HERE - INIT MATCHES NOT ACTUALLY A MATCHING
    def __init__(self, init_matches=set([])):
        self.edges = init_matches
        self.marks, self.matches = {}, {}
        for match in init_matches:
            v,u = match
            self.matches[v] = u; self.matches[u] = v
            self.marks[match] = False
    def size(self):
        return len(self.edges)
    def add_edge(self, edge, mark=False):
        if edge in self.edges():
            raise ValueError('Match already exists in matching.')
        v, u = edge
        self.edges.add(edge)
        self.matches[v] = u
        self.matches[u] = v
        self.marks[edge] = mark
    def remove_match(self, edge, raise_error=True):
        if not self.edge_in_matching(edge) and raise_error:
            raise KeyError('Edge does not exist in matching.')
        self.edges -= {edge,edge[::-1]}
        try: self.marks.pop(edge)
        except KeyError: self.marks.pop(edge[::-1])
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
        # Make the ordering of the edge tuple consistent between aug_path and this matching
        transposed = [(e,e[::-1]) for e in aug_path.edges if e[::-1] in self.edges]
        if len(transposed) > 0:
            remove, add = zip(*(transposed))
            aug_path.edges = aug_path.edges - set(remove) | set(add)
        # Augment the matching
        augmentation = (self.edges - aug_path.edges) | (aug_path.edges - self.edges)
        return Matching(augmentation)
    def covered_vertices(self):
        return set(self.matches.keys())
    def contract_blossom(self, edges, make_new=False):
        if make_new:
            M_prime = copy.deepcopy(self)
            blossom_vertices = set([e[0] for e in edges] + [e[1] for e in edges])
            # finding the base of the blossom, should be unmatched
            # TODO: IS IT ACTUALLY ALWAYS UNMATCHED...?
            for v in blossom_vertices:
                if self.get_matched_vertex(v, raise_error=False) is None:
                    blossom_base = v; break
            # remove the matches within the blossom
            for v in blossom_vertices - {blossom_base}:
                match = M_prime.get_matched_edge(v, raise_error=False)
                if match is None: continue
                M_prime.remove_match(match)
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
        else: raise KeyError('Adding edge to tree violates connectedness of graph.')
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
            path_edges.append((vertex,parent))
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
