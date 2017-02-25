from graphs import Graph, Tree, Path, Matching

def lift_augmenting_path(G, P_prime):
    raise Exception('unimplemented')

def find_augmenting_path(G, M):
    F = Forest() # a set of trees
    G.unmark_all()
    M.mark_all()

    exposed_vertices = G.get_vertices() - M.covered_vertices()
    for v in exposed_vertices:
        forest.sprout(Tree(v))

    while True:
        v,v_tree = F.get_unmarked_vertex()
        if v is None: break
        while True:
            w = G.get_unmarked_edge(v)
            if w is None: break
            w_tree = F.get_tree(w)
            if w_tree is None:
                x = M.get_matched_vertex(w)
                v_tree.add_edge((v,w))
                v_tree.add_edge((w,x))
            elif len(w_tree.root_path(w)) % 2 == 0:
                if v_tree.root != w_tree.root: # found augmenting path
                    P = Path(v_tree.root_path(v) | {(v,w)} | w_tree.root_path(w))
                    return P
                else:
                    blossom_edges = v_tree.get_path(v,w) | {(v,w)}
                    G_prime = G.contract(tuple(blossom_edges), make_new=True)
                    M_prime = M.contract(blossom_edges, make_new=True)
                    P_prime = find_augmenting_path(G_prime, M_prime)
                    P = lift_augmenting_path(G, P_prime)
                    return P
            G.mark_edge((v,w), True)
        G.mark_vertex(v, True)
        
def find_maximum_matching(G, M):
    P = find_augmenting_path(G, M)
    if P.length() == 0: return M
    else:
        M_augmented = M.augment(P)
        find_maximum_matching(G, M_augmented)

if __name__ == '__main__':
    print 'test unimplemented yet'
