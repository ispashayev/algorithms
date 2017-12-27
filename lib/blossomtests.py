def get_blossom_tests():
  with open('lib/blossom-tests.dat', 'r') as tests:
    edge_sets = []; edges = False
    init_matchings = []; matching = False
    for line in tests:
      line = line.strip()
      if line == '':
        edge_sets.append(curr_edges)
        init_matchings.append(init_matching)
      elif line[:4] == 'TEST':
        i = int(line.split()[1]) - 1
        curr_edges = set([])
        init_matching = set([])
      elif line == 'EDGES':
        edges, matching = True, False
      elif line == 'INIT MATCHING':
        matching, edges = True, False
      else:
        if edges:
          to_insert_in = curr_edges
        elif matching:
          to_insert_in = init_matching
        to_insert_in.add(tuple(line[1:-1].split(',')))
  return zip(edge_sets, init_matchings)

if __name__ == '__main__':
  print(get_blossom_tests())