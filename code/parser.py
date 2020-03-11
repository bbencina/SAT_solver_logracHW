
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

def dpll(cnf, assign):
    print('Checking end condition...')
    if len(cnf) == 0:
        return True, assign
    elif any([len(dis) == 0 for dis in cnf]):
        return False, assign
    print('Selecting new literal...')
    lit = select_lit(cnf)
    # true branch
    print('===TRUE===')
    new_cnf = []
    print(lit, 'True')
    print('Constructing new cnf...')
    new_cnf = [dis for dis in cnf if lit not in dis]
    print('Step 1: ', new_cnf)
    new_cnf = [dis.difference({-lit}) for dis in new_cnf]
    print('Step 2: ', new_cnf)
    print('Assign: ', assign)
    sat, assign = dpll(new_cnf, {**assign, lit:True})
    if sat:
        return sat, assign
    else:
        del assign[lit]
    # false branch
    print('===FALSE===')
    new_cnf = []
    print(lit, 'False')
    print('Constructing new cnf...')
    new_cnf = [dis for dis in cnf if -lit not in dis]
    print('Step 1: ', new_cnf)
    new_cnf = [dis.difference({lit}) for dis in new_cnf]
    print('Step 2: ', new_cnf)
    print('Assign: ', assign)
    sat, assign = dpll(new_cnf, {**assign, lit:False})
    if sat:
        return sat, assign
    else:
        del assign[lit]

def main():
    fname = r'..\test\basic.txt'
    cnf = dimacs_to_cnf(fname)
    print(cnf)
    print(dpll(cnf, {}))

main()
