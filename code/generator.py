def to_dimacs(i, j, k):
    '''Auxiliary function calculating the number of the literal.'''
    # vertex i is colored with color j, k is the number of all colors
    return (i - 1) * k + j

def gen(V, E, k):
    '''Generates a cnf to solve the k-colourability problem for the graph (V,E).
    :param V - set of vertices
    :param E - set of edges
    :param k - number of colours we want to use

    :returns cnf - a list of sets (each set one disjunction)
    '''
    cnf = []
    # each node of the graph has to be colored by one of k colors
    for i in V:
        vi = set()
        for j in range(1, k + 1):
            vi.add(to_dimacs(i, j, k + 1))
        cnf.append(vi)
    # no two adjacent vertices have the same coloring
    for (i, j) in E:
        for l in range(1, k + 1):
            vij = set()
            vij.add(-to_dimacs(i, l, k))
            vij.add(-to_dimacs(j, l, k))
            cnf.append(vij)
    return cnf
