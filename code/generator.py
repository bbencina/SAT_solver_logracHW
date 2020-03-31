import argparse
import random as rd
import sys
import time
import os

import solver

GRAPH_PATH = os.path.join('..', 'graphs')

def generate_graph(n):
    V = [*range(1, n + 1)]
    E = []
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            if bool(rd.getrandbits(1)):
                E.append((i, j))
    return V, E

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

def cnf_to_dimacs(cnf, n_lits, n_clauses, file_name, params=''):
    '''Creates a dimacs file from a given cnf.
    :param cnf - a list of sets (each set one disjunction)
    :param n_lits - number of literals we want in the formula (some may be skipped)
    :param n_clauses - number of clauses we want the formula to contain
    :param file_name - the name of the file we want to create
    :param params - additional information we want to add as a comment, empty by default

    :returns None
    '''
    dimacs = open(file_name, 'w+')
    dimacs.write('c This file was generated automatically by generator.py\n')
    dimacs.write('c\n')
    dimacs.write('c params: ' + params + '\n')
    dimacs.write('p cnf: {0} {1}\n'.format(str(n_lits), str(n_clauses)))
    for dis in cnf:
        for lit in dis:
            dimacs.write(str(lit) + ' ')
        dimacs.write('0\n')
    dimacs.close()

def main():
    '''Main body of the program. Gets automatically called if this script is called from the command line.
    '''
    # create directory for dumping
    if not os.path.exists(GRAPH_PATH):
        os.mkdir(GRAPH_PATH)

    # parse command line arguments
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('num_ver', help='number of vertices', metavar='num-ver')
    cli_parser.add_argument('num_col', help='number of colors', metavar='num-col')
    cli_parser.add_argument('repeat', help='number of repetitions', metavar='rep')
    cli_args = cli_parser.parse_args()

    n_ver = int(cli_args.num_ver)
    k = int(cli_args.num_col)
    rep = int(cli_args.repeat)

    for i in range(rep):
        try:
            print('Case {0}/{1}: '.format(str(i+1), str(rep)), end='')
            V, E = generate_graph(n_ver)
            cnf = gen(V, E, k)
            n_lits = to_dimacs(n_ver, k, k)
            n_clauses = len(cnf)

            time_begin = time.time()
            sat, vals = solver.dpll(cnf, {}, True, True)
            time_end = time.time()

            print("DPLL algorithm ran for {:f} seconds: ".format(time_end-time_begin), end='')

            if sat:
                print("SAT")
                check = solver.verify_solution(cnf,vals)
                if check:
                    print("Solution is valid.")
                    base_name = str(n_lits) + '_' + str(n_clauses) + '_' + str(hash(str(cnf)))
                    file_name = os.path.join(GRAPH_PATH, base_name)
                    cnf_to_dimacs(cnf, n_lits, n_clauses, file_name + '.txt', '')
                    solver.make_solution_file(file_name + '_solution.txt', vals)
                    print("Solution written to {}".format(file_name + '_solution.txt'))
                else:
                    print("Solution NOT valid!")

            else:
                print("NONSAT")
        except:
            continue

if __name__ == '__main__':
    main()
