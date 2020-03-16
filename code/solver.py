#!/usr/bin/python3

import sys
#import os

from functools import reduce

def parse_dimacs(dimacs_file):
    cnf = []
    for line in dimacs_file:
        if line[0] in ('c', 'p'):
            continue
        literals = set(map(int, line.strip().split(' ')[:-1]))
        cnf.append(literals)
    return cnf

def make_solution_file(f_name, vals):
    with open(f_name, 'w+') as f_handle:
        if not vals:
            f_handle.write('0')
            return
        for lit in vals:
            coef = 1 if vals[lit] else -1
            f_handle.write(str(coef*lit))
            f_handle.write(' ')


def select_lit(cnf):
    for dis in cnf:
        for lit in dis:
            return abs(lit)

def assign_lit(cnf, lit, val):
    coef = 1 if val else -1
    new_cnf = [dis for dis in cnf if coef*lit not in dis]
    new_cnf = [dis.difference({-coef*lit}) for dis in new_cnf]
    return new_cnf

def assign_unit_clauses(cnf, assignments={}):

    unit_clauses = [dis for dis in cnf if len(dis) == 1]

    if not unit_clauses:
        return cnf, assignments

    signed_lit = next(iter(unit_clauses[0]))
    lit = abs(signed_lit)
    val = signed_lit > 0

    new_cnf = assign_lit(cnf, lit, val)

    return assign_unit_clauses(new_cnf, {**assignments, lit:val})

def dpll(cnf, assign={}):

    # empty cnf is true
    if len(cnf) == 0:
        return True, assign

    # cnf containing any empty disjunction is false
    if any([len(dis) == 0 for dis in cnf]):
        return False, None

    # unit propagation
    cnf, new_assign = assign_unit_clauses(cnf)
    assign = {**assign, **new_assign}

    if len(cnf) == 0:
        return True, assign

    if any([len(dis) == 0 for dis in cnf]):
        return False, None


    # pure literal elimination: TODO


    # branching literal assignment
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


def verify_solution(cnf, vals):

    assign = lambda l : vals[l] if (l > 0) else not vals[-l]

    for dis in cnf:
        if not reduce((lambda x,y : x or y), map(assign, dis)):
            return False

    return True


def main(argv):

    if (len(argv) != 3):
        print("Usage: {} <dimacs-file> <output-file>".format(argv[0]))
        return

    in_file_path = argv[1]
    out_file_path = argv[2]

    with open(in_file_path, 'r') as file_handle:
        #print('Parsing input file...', end='')
        cnf = parse_dimacs(file_handle)

        sat, vals = dpll(cnf)

        if sat:
            print("SAT")
            check = verify_solution(cnf,vals)
            if check:
                print("Solution is valid.")
            else:
                print("Solution NOT valid!")

            make_solution_file(out_file_path, vals)

        else:
            print("Not SAT")

#        print('Done.')
#        print('Checking satisfiability...', end='')
#        sat, vals = dpll(cnf)
#        print('Done.')
#        head, tail = os.path.split(in_file_path)
#        root_ext = os.path.splitext(tail)
#        o_file_name = root_ext[0] + '_solution' + root_ext[1]
#        if not sat:
#            make_solution_file(o_file_name, {})
#            print("Not satisfiable...wrote solution to " + o_file_name + ".")
#            return
#
#        make_solution_file(o_file_name, vals)
#        print('Satisfiable...wrote solution to ' + o_file_name + '.')

if __name__ == "__main__":
    main(sys.argv)
