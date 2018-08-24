'''
Author:     Iskandar Pashayev
Purpose:    Implements graph theoretic data structures.
'''

import copy
import random
from collections import defaultdict

class Graph(object):
  def __init__(self):
    '''
    A dictionary mapping vertices to adjacent vertices. Keys can be any
    immutable data type. Values are stored as sets of other vertex labels.
    '''
    self.graph = {}
    self.marks = {} # marks both vertices and edges
  
  '''
  Adds a vertex to the graph. Does not add any neighbors to this vertex. If
  raise_error indicator is set (default True), will fault if vertex is already
  in the graph. Mark is a T/F indicator variable used in Blossom algorithm.
  '''
  def add_vertex(self, vertex, mark=False, raise_error=True):
    if vertex in self.graph:
      if raise_error:
        raise KeyError('Vertex already exists in graph.')
    self.graph[vertex] = set()
    self.marks[vertex] = mark
  
  '''
  Adds a collection of vertices to the graph, potentially erroring out if any
  of the vertices already exists in the graph. Vertices can be any iterable.
  '''
  def add_vertices(self, vertices, raise_error=True):
    for v in vertices:
      self.add_vertex(v, raise_error=raise_error)
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

  '''
  Adds an edge to the graph. If raise_error indicator is set (default True),
  will fault if either of endpoints of the edge are not in the graph. If an
  endpoint is not in the graph but the raise_error flag is explicitly not set,
  then the vertex is added with the default add_vertex method.
  '''
  def add_edge(self, edge, mark=False, raise_error=True):
    v, u = edge
    if v not in self.graph:
      self.add_vertex(v, raise_error=raise_error)
    if u not in self.graph:
      self.add_vertex(u, raise_error=raise_error)
    self.graph[v].add(u)
    self.graph[u].add(v)
    self.marks[edge] = mark
    self.marks[v] = mark
    self.marks[u] = mark
  
  '''
  Adds a collection of edges to the graph.
  '''
  def add_edges(self, edge_set, mark=False):
    for edge in edge_set:
      self.add_edge(edge, mark=mark)
  
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

  def contract_blossom(self, blossom, make_new=False):
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
  def get_path(self, s, t, search='BFS'):
    if not self.vertex_exists_in_graph(s) or not self.vertex_exists_in_graph(t):
      raise KeyError('Cannot compute path: vertices not in graph.')
    if search == 'BFS':
      parents = {}
      for v in self.get_vertices():
        visited[v] = False
      visited[s] = True
      q = self.get_neighbors(s)
      while len(q) > 0:
        current = q.pop()
        for neighbor in self.get_neighbors(current):
          if neighbor not in visited:
            visited[neighbor] = True
            q.insert(0, neighbor)
            parent[neighbor] = current
      if visited[t]:
        st_path = set([])
        current = s
        while current != t:
          st_path |= (current,parents[current])
          current = parents[current]
        return Path(st_path)
    else:
      raise Exception('Other search types for finding paths in graph are unimplemented.')

  '''
  Static method for verifying an isomorphism from graph G_1 to graph G_2 is
  valid. g1_TO_g2 is a dictionary translating vertex labels from G_1 to vertex
  labels in G_2.
  '''
  @staticmethod
  def is_isomorphism(G_1, G_2, g1_TO_g2):
    for v,neighbors in G_1.graph.items():
      translated_v = g1_TO_g2[v]
      translated_neighbors = set(map(lambda x: g1_TO_g2[x], neighbors))
      g2_group = G_2.graph[translated_v]
      if len(translated_neighbors ^ g2_group) > 0:
        # There are vertices that are not in both sets.
        return False
    return True

  @staticmethod
  def compute_isomorphism(G_1, G_2):
    if len(G_1.graph) != len (G_2.graph):
      # different number of vertices => no isomorphism
      return None
    degree_dist_1, degree_dist_2 = defaultdict(list), defaultdict(list)
    for v_1,v_2 in zip(G_1.graph, G_2.graph):
      degree_dist_1[len(G_1.graph[v_1])].append(v_1)
      degree_dist_2[len(G_2.graph[v_2])].append(v_2)
    if len(degree_dist_1) != len(degree_dist_2):
      # different degree distribution => no isomorphism
      return None
    for deg_1,deg_2 in zip(degree_dist_1,degree_dist_2):
      if deg_1 != deg_2:
        return None
      if len(degree_dist_1[deg_1]) != len(degree_dist_2[deg_2]):
        return None

    '''
    Now that we have checked the basic constraints for an isomorphism the
    next step is to exhaustively generate feasible isomorphisms and verifying
    them. If we find one that works, return it!
    
    To generate an isomorphism. We utilize the degree distribution. In any
    isomorphism, it must be the case that the degree of a vertex stays the
    same. So we will only try mappings that preserves the degree distribution.
    '''

    def _get_random_mapping(degree_dist_1, degree_dist_2):
      g1_TO_g2 = {}
      for deg,vertices in degree_dist_2.items():
        shuffled = random.sample(vertices, len(vertices))
        for v,u in zip(degree_dist_1[deg], shuffled):
          g1_TO_g2[v] = u
      return g1_TO_g2

    ctr = 0
    while ctr < 1000:
      mapping = _get_random_mapping(degree_dist_1, degree_dist_2)
      if Graph.is_isomorphism(G_1, G_2, mapping):
        return mapping
      ctr += 1

    return None

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
    transposed = [(e,e[::-1]) for e in aug_path.edges if e[::-1] in self.edges] # see if you can cut this out
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
  # TODO: I dont think I need this function, and can just call super.
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

class Network(Graph):
  '''
  Constructor for initializing a Network. If parameters are given, construct
  the network from their specification. Arguments specify parameters:
  1) V - vertex set
  2) E - edge set
  3) s - vertex in V that is the source
  4) t - vertex in V that is the sink
  5) c - a capacity function; dictionary mapping each edge to an integer
  '''
  def __init__(self, V=None, E=None, s=None, t=None, c=None):
    if any([V, E, s, t, c]):
      self._validate_specified_parameters(V, E, s, t, c)
      self._initialize_from_given(V, E, s, t, c)
    else:
      super(Network, self).__init__()
      self.c, self.flow = {}, {}

  '''
  Helper method for constructor in sanitizing parameters. If the user passes
  network parameters, he must specify either all of them, or none. The meanings
  of the arguments for this method are the exact same as for the constructor.
  '''
  def _validate_specified_parameters(self, V, E, s, t, c):
    assert V is not None, 'Network parameters missing vertex set.'
    assert E is not None, 'Network parameters missing edge set.'
    assert s is not None, 'Network parameters missing source.'
    assert t is not None, 'Network parameters missing sink.'
    assert c is not None, 'Network parameters missing capacity function.'
    assert s in V, 'Specified source not in specified vertex set.'
    assert t in V, 'Specified sink not in specified vertex set.'
    assert s != t, 'The source and the sink cannot be the same.'
    capacities = set(c.keys)
    intersection_len = len(E & capacities)
    assert intersection_len == len(capacities), 'Invalid capacity function.'
    assert intersection_len == len(E), 'Invalid capacity function.'

  def _initialize_from_given(V, E, s, t, c):
    super(Network, self).add_vertices(V)
    super(Network, self).add_edges(E)
    self.E = E
    self.s = s
    self.t = t
    self.c = c

  def get_source(self):
    return self.s
  def get_sink(self):
    return self.t
  def add_edge(self, e, capacity):
    super(Network, self).add_edge(e)
    self.c[e] = capacity
  def add_edges(self, edge_capacities):
    for edge,capacity in edge_capacities:
      self.add_edge(edge, capacity)
  def remove_edge(self, edge):
    super(Network, self).remove_edge(edge)
    self.c.pop(edge)

class flow(object):
  def __init__(self, network):
    if network is None:
      raise Exception('Cannot have a flow for an empty network.')
    if len(network.V) == 0:
      raise Exception('Cannot have a flow for an empty network.')
    if network.get_source() is None or network.get_sink() is None:
      raise Exception('Network does not have a source or a sink.')
    self.network = network
    self.flow = {}
    for edge in self.network.capacity_fn.keys():
      self.flow[edge] = 0
    self.flow_value = 0
  def get_value(self, edge=None):
    if edge is None:
      return self.flow_value
    if not self.network.edge_exists_in_graph(edge):
      raise KeyError('Edge does not exist in the network.')
    try: return self.flow[edge]
    except: return self.flow[edge[::-1]]
  def add(self, edge, value):
    self.flow[edge] = value
    self.flow_value += path_flow
