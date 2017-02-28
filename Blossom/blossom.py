from graphs import Graph, Tree, Path, Matching, Forest

def lift_augmenting_path(G, P_prime, M, B, base):
    blossom_matching, blossom_unmatching = M.edges & B, B - M.edges
    blossom_vertices = set([e[0] for e in B] + [e[1] for e in B])
    end_1, end_2 = P_prime.get_ends()
    current, visited = end_1, {end_1}
    lifted_path = Path()
    while True:
        if current == end_2: break
        visited.add(current)
        neighbor = (P_prime.get_neighbors(current) - visited).pop()
        found_blossom = False
        if len(neighbor) > 1: # found a blossom
            found_blossom = True
            for edge in blossom: # verify this is the blossom we want
                if edge or edge[::-1] not in B:
                    found_blossom = False
                    break
        if found_blossom:
            next_vertex = (P_prime.get_neighbors(neighbor) - {current}).pop()
            lifted_path.add_edge((current, base))
            branch_one_current, branch_two_current = blossom_vertices & G.get_neighbors(base)
            branch_one = set((base,branch_one_current)),
            branch_two = set((base,branch_two_current))
            for k in range(len(blossom)/2 - 1):
                branch_next_one = blossom_vertices & G.get_neighbors(branch_one_current)
                branch_next_one = (branch_next_one - {branch_one_current}).pop()
                branch_next_two = blossom_vertices & G.get_neighbors(branch_two_current)
                branch_next_two = (branch_next_two - {branch_two_current}).pop()
                branch_one |= {(branch_one_current, branch_next_one)}
                branch_two |= {(branch_two_current, branch_next_two)}
                branch_one_current, branch_two_current = branch_next_one, branch_next_two
            blossom_exit_one_neighbors = G.get_neighbors(branch_one_current)
            blossom_exit_two_neighbors = G.get_neighbors(branch_two_current)
            if len(blossom) % 4 == 1:
                if next_vertex in G.get_neighbors(branch_one_current):
                    lifted_path.add_edges(branch_one | {(branch_one_current,next_vertex)})
                elif next_vertex in G.get_neighbors(branch_two_current):
                    lifted_path.add_edges(branch_two | {(branch_two_current,next_vertex)})
                else:
                    raise Exception('Blossom exits not adjacent to vertex after blossom.')
            elif len(blossom) % 4 == 3:
                lifted_path.add_edge((branch_one_current,branch_two_current))
                if next_vertex in G.get_neighbors(branch_one_current):
                    lifted_path.add_edges(branch_two | {(branch_one_current,next_vertex)})
                elif next_vertex in G.get_neighbors(branch_two_current):
                    lifted_path.add_edges(branch_one | {(branch_two_current,next_vertex)})
                else:
                    raise Exception('Blossom exits not adjacent to vertex after blossom.')
            else:
                raise Exception('Blossom is not an odd cycle.')
            current = next_vertex
        else:
            lifted_path.add_edge((current,neighbor))
            current = neighbor
    return lifted_path

def find_augmenting_path(G, M):
    F = Forest() # a set of trees
    G.unmark_all()
    for e in M.edges:
        G.mark_edge(e, False)
    M.mark_all() # not necessary I think

    exposed_vertices = G.get_vertices() - M.covered_vertices()
    for v in exposed_vertices:
        F.plant(Tree(v))
    print 'forest initialized to tree roots',[tree.root for tree in F.trees]
    while True:
        v,v_tree = F.get_unmarked_vertex()
        if v is None:
            print 'unable to find unmarked vertex in forest, returning empty path'
            break
        print 'found unmarked vertex',v,'in forest tree rooted at',v_tree.root
        while True:
            w = G.get_unmarked_edge(v)
            if w is None:
                print 'unable to find unmarked edge incident to',v
                break
            w_tree = F.get_tree(w)
            print 'found unmarked edge incident to',v,'(neighbor is',w,')'
            if w_tree is None:
                x = M.get_matched_vertex(w)
                v_tree.add_edge((v,w))
                v_tree.add_edge((w,x))
                print 'vertex',w,'is matched to',x
                print 'adding',(v,w),'and',(w,x),'to',v_tree.root
            elif w_tree.elevation(w) % 2 == 0:
                print 'neighbor along this edge is in forest tree rooted at',w_tree.root
                if v_tree.root != w_tree.root: # found augmenting path
                    P = Path(v_tree.root_path(v) | {(v,w)} | w_tree.root_path(w))
                    print v,'and',w,'are in different trees in the forest.'
                    print 'Returning augmenting path with edge set',P.edges,'and ends',P.end_1,P.end_2
                    return P
                else:
                    print v,'and',w,'are in same tree in the forest.'
                    B = v_tree.get_path(v,w) | {(v,w)} # B is the blossom
                    print 'so contracting graph and matching with blossom edges',B
                    G_prime = G.contract_blossom(tuple(B), make_new=True) # tuple of tuples
                    M_prime = M.contract_blossom(tuple(B), make_new=True)
                    P_prime = find_augmenting_path(G_prime, M_prime)
                    print 'found augmenting path for contracted graph with blossom edges',# BUG:
                    print 'the path has edges',P_prime.edges,'and ends',P_prime.end_1,P_prime.end_2
                    P = lift_augmenting_path(G, P_prime, B, v)
                    print 'returning lifted path with edges',P.edges,'and ends',P.end_1,P.end_2
                    return P
            #v_tree.mark_edge((v,w), True)
            G.mark_edge((v,w), True)
        v_tree.mark_vertex(v, True)
        #G.mark_vertex(v, True) # not necessary I think

    return Path()

def find_maximum_matching(G, M):
    P = find_augmenting_path(G, M)
    if P.length() == 0:
        print 'Unable to find augmenting path. Matching',M.edges,'is maximum.'
        return M
    else:
        M_augmented = M.augment(P)
        print 'Found augmenting path. Matching augmented to',M_augmented.edges
        return find_maximum_matching(G, M_augmented)

if __name__ == '__main__':
    G= Graph()
    edge_set = {(0,3),(0,4),(0,5)}
    edge_set |= {(1,2),(1,4),(1,5)}
    edge_set |= {(2,5)}
    edge_set |= {(3,4),(3,5)}
    G.add_edges(edge_set)
    M = find_maximum_matching(G, Matching())
    print 
