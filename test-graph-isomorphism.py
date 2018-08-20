from lib.Graphs import Graph

if __name__ == '__main__':
  print 'This is a module that tests the graph isomorphism function of the Graph library'
  
  V_A = ['A', 'B', 'C', 'D']
  V_B = [1, 2, 3,4]

  E_A = [('A','B'), ('B','C'), ('C','D'), ('D','A')]
  E_B = [(1,2), (1,4), (2,3), (3,4)]

  G_1, G_2 = Graph(), Graph()
  G_1.add_vertices(V_A); G_1.add_edges(E_A)
  G_2.add_vertices(V_B); G_2.add_edges(E_B)

  mapping = Graph.compute_isomorphism(G_1, G_2)
  if mapping is None:
    print 'Unable to find an isomorphism.'
  else:
    print 'Found isomorphism:'
    print mapping