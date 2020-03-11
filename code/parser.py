
def dimacs_to_cnf(filename):
    cnf = []
    f_handle = open(filename, 'r')
    for line in f_handle:
        if line[0] in {'c', 'p'}:
            continue
        literals = set(map(int, line.strip().split(' ')[:-1]))
        cnf.append(literals)
    return cnf

def select_lit(cnf):
    for dis in cnf:
        for lit in dis:
            return abs(lit)

def assign_lit(cnf, lit, val):
    coef = 1 if val else -1
    new_cnf = []
    new_cnf = [dis for dis in cnf if coef*lit not in dis]
    new_cnf = [dis.difference({-coef*lit}) for dis in new_cnf]
    return new_cnf

def dpll(cnf, assign={}):
    if len(cnf) == 0:
        return True, assign
    elif any([len(dis) == 0 for dis in cnf]):
        return False, None
    lit = select_lit(cnf)
    # true branch
    new_cnf = assign_lit(cnf, lit, True)
    sat, vals = dpll(new_cnf, {**assign, lit:True})
    if sat:
        return sat, vals
    # false branch
    new_cnf = assign_lit(cnf, lit, False)
    sat, vals = dpll(new_cnf, {**assign, lit:False})
    if sat:
        return sat, vals
    return False, None

def main():
    fname = r'..\..\Homework Files-20200311\sudoku_easy.txt'
    cnf = dimacs_to_cnf(fname)
    print(dpll(cnf, {}))

main()
