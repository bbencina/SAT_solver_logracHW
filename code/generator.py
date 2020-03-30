def to_dimacs(i, j, k):
    return (i - 1) * k + j

def gen(V, E, k):
    cnf = []
    for i in V:
        vi = set()
        for j in range(1, k + 1):
            vi.add(to_dimacs(i, j, k + 1))
        cnf.append(vi)
    for (i, j) in E:
        for l in range(1, k + 1):
            vij = set()
            vij.add(-to_dimacs(i, l, k))
            vij.add(-to_dimacs(j, l, k))
            cnf.append(vij)
    return cnf
