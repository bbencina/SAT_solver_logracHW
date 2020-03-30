#!/usr/bin/python3

import argparse
import random as rd
import sys
import time
import os

import solver

GEN_PATH = os.path.join('..', 'randgenerated')

def generate_cnf(n_lits, n_clauses, dis_size):
    cnf = []
    for i in range(n_clauses):
        dis = set()
        d_size = rd.randint(1, dis_size)
        for j in range(d_size):
            lit = rd.randint(1, n_lits)
            sign_gen = rd.randint(1, 2)
            sign = 1 if sign_gen == 1 else -1
            dis.add(sign*lit)
        cnf.append(dis)
    return cnf

def cnf_to_dimacs(cnf, n_lits, n_clauses, dis_size, file_name, params=''):
    dimacs = open(file_name, 'w+')
    dimacs.write('c This file was generated automatically by generator.py\n')
    dimacs.write('c\n')
    dimacs.write('c params: ' + params + '\n')
    dimacs.write('p cnf: {0} {1}, max disjunction size {2}\n'.format(str(n_lits),
                                                                   str(n_clauses),
                                                                   str(dis_size)))
    for dis in cnf:
        for lit in dis:
            dimacs.write(str(lit) + ' ')
        dimacs.write('0\n')
    dimacs.close()

def main():
    if not os.path.exists(GEN_PATH):
        os.mkdir(GEN_PATH)

    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('num_lits', help='number of literals', metavar='num-lits')
    cli_parser.add_argument('num_clauses', help='number of clauses', metavar='num-clauses')
    cli_parser.add_argument('dis_size', help='max size of disjunctions', metavar='dis-size')
    cli_parser.add_argument('repeat', help='number of repetitions', metavar='rep')
    cli_args = cli_parser.parse_args()

    n_lits = int(cli_args.num_lits)
    n_clauses= int(cli_args.num_clauses)
    dis_size = int(cli_args.dis_size)
    rep = int(cli_args.repeat)

    for i in range(rep):
        print('Case {0}/{1}: '.format(str(i+1), str(rep)), end='')
        cnf = generate_cnf(n_lits, n_clauses, dis_size)

        time_begin = time.time()
        sat, vals = solver.dpll(cnf, {}, True, True)
        time_end = time.time()

        print("DPLL algorithm ran for {:f} seconds: ".format(time_end-time_begin), end='')

        if sat:
            print("SAT")
            check = solver.verify_solution(cnf,vals)
            if check:
                print("Solution is valid.")
                base_name = str(n_lits) + '_' + str(n_clauses) + '_' + str(dis_size) + '_' + str(hash(str(cnf)))
                file_name = os.path.join(GEN_PATH, base_name)
                cnf_to_dimacs(cnf, n_lits, n_clauses, dis_size, file_name + '.txt', '')
                solver.make_solution_file(file_name + '_solution.txt', vals)
                print("Solution written to {}".format(file_name + '_solution.txt'))
            else:
                print("Solution NOT valid!")

        else:
            print("NONSAT")

if __name__ == '__main__':
    main()
