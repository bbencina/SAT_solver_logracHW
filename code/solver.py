#!/usr/bin/python3

import argparse
import time
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

def assign_multiple_literals(cnf, assignments):

    if not assignments:
        return cnf

    keys = assignments.keys()

    """
    Disjunctive clauses should be removed from cnf when:

    l is not negated (i.e. l>0), and abs(l) is assigned True
    l is negated (i.e. l<0), and abs(l) is assigned False

    This amounts to checking (l>0) XNOR assignments[abs(l)]

    The code fails without converting the filtered cnf back to list.
    """
    test_dis_for_removal = lambda dis : not any([l for l in dis if abs(l) in keys and not (l>0)^(assignments[abs(l)])])

    new_cnf = list(filter(test_dis_for_removal, cnf))

    """
    Literals should be removed from dis clauses of cnf when:

    l is negated (i.e. l<0), and abs(l) is assigned True
    l is not negated (i.e. l>0), and abs(l) is assigned False

    This amouunts to checking (l<0) XNOR assignments[abs(l)]

    new_cnf is generated via set comprehension to avoid duplicate dis clauses.
    The inner sets (i.e. dis) need to be immutable for this to work.
    Otherwise the code crashes with "TypeError: unhashable type: 'set'"
    Hence frozenset is used in place of set.
    """
    test_lit_for_removal = lambda l : (abs(l) in keys) and not (l<0)^(assignments[abs(l)])

    new_cnf = list({frozenset(dis.difference({l for l in dis if test_lit_for_removal(l)})) for dis in new_cnf})

    return new_cnf


"""
def assign_unit_clauses(cnf, assignments={}):

    unit_clauses = [dis for dis in cnf if len(dis) == 1]

    if not unit_clauses:
        return cnf, assignments

    signed_lit = next(iter(unit_clauses[0]))
    lit = abs(signed_lit)
    val = signed_lit > 0

    new_cnf = assign_lit(cnf, lit, val)

    return assign_unit_clauses(new_cnf, {**assignments, lit:val})
"""

def assign_unit_clauses(cnf):

    assignments = { abs(lit) : (lit > 0) for dis in cnf for lit in dis if len(dis) == 1 }

    if assignments:
        return assign_multiple_literals(cnf, assignments), assignments

    return cnf, {}

def assign_pure_literals(cnf):

    signed_literals = set().union(*cnf)

    pure_literals = {lit for lit in signed_literals if -lit not in signed_literals}

    assignments = {abs(lit) : (lit > 0) for lit in pure_literals}

    if assignments:
        new_cnf = assign_multiple_literals(cnf,assignments)
        return new_cnf, assignments

    return cnf, {}


def dpll(cnf, assign={}, unit_prop=True, purelit_elim=True):

    # empty cnf is true
    if len(cnf) == 0:
        return True, assign

    # cnf containing any empty disjunction is false
    if any([len(dis) == 0 for dis in cnf]):
        return False, None


    # unit propagation
    if unit_prop:
        cnf, new_assign = assign_unit_clauses(cnf)
        assign = {**assign, **new_assign}

        if len(cnf) == 0:
            return True, assign

        if any([len(dis) == 0 for dis in cnf]):
            return False, None

    # pure literal elimination
    if purelit_elim:
        cnf, new_assign = assign_pure_literals(cnf)
        assign = {**assign, **new_assign}

        if len(cnf) == 0:
            return True, assign

        if any([len(dis) == 0 for dis in cnf]):
            return False, None


    # branching literal assignment
    lit = select_lit(cnf)

    # true branch
    new_cnf = assign_lit(cnf, lit, True)
    sat, vals = dpll(new_cnf, {**assign, lit:True}, unit_prop, purelit_elim)
    if sat:
        return sat, vals

    # false branch
    new_cnf = assign_lit(cnf, lit, False)
    sat, vals = dpll(new_cnf, {**assign, lit:False}, unit_prop, purelit_elim)
    if sat:
        return sat, vals

    return False, None


def verify_solution(cnf, vals):

    assign = lambda l : vals[l] if (l > 0) else not vals[-l]
    #assign = lambda l : (vals[l] if (l > 0) else not vals[-l]) if abs(l) in vals.keys() else True

    for dis in cnf:
        if not reduce((lambda x,y : x or y), map(assign, dis)):
            return False

    return True


def main():

    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('input_file', help='DIMACS file containing CNF', metavar='input-file')
    cli_parser.add_argument('-o', help='output file to write solution if SAT', metavar='output-file')
    cli_parser.add_argument('-nU', '--no-unit-prop', help='disable unit propagation', action='store_true')
    cli_parser.add_argument('-nP', '--no-pure-elim', help='disable pure literal elimination', action='store_true')
    cli_args = cli_parser.parse_args()

    in_file_path = cli_args.input_file
    out_file_path = cli_args.o
    unit_prop = not cli_args.no_unit_prop
    purelit_elim = not cli_args.no_pure_elim

    with open(in_file_path, 'r') as file_handle:
        print("Parsing input file {}\n".format(in_file_path))
        cnf = parse_dimacs(file_handle)

        status_string = lambda x : "ENABLED" if x else "DISABLED"
        print("Unit propagation: {}".format(status_string(unit_prop)))
        print("Pure literal elimination: {}\n".format(status_string(purelit_elim)))
        print("Attempting solution...")

        time_begin = time.time()
        sat, vals = dpll(cnf, {}, unit_prop, purelit_elim)
        time_end = time.time()

        print("DPLL algorithm ran for {:f} seconds: ".format(time_end-time_begin), end='')

        if sat:
            print("SAT")
            check = verify_solution(cnf,vals)
            if check:
                print("Solution is valid.")
            else:
                print("Solution NOT valid!")

            if out_file_path:
                make_solution_file(out_file_path, vals)
                print("Solution written to {}".format(out_file_path))

        else:
            print("NONSAT")

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
    main()
