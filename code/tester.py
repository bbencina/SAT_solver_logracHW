#!/usr/bin/python3

import sys
import solver

def vals_from_sol(sol_file_name):
    with open(sol_file_name, 'r') as s_file:
        content = s_file.read().strip()
        if content[0] == '0':
            return {}
        int_sols = set(map(int, content.split(' ')))
        return int_sols

def check_solution(cnf, vals):
    # go through each disjunction
    for dis in cnf:
        dis_flag = False
        # scan each literal
        for lit in dis:
            # if one literal is correct, the whole disjunction is true -> break
            if (-1)*lit not in vals:
                dis_flag = True
                break
        # if one disjunction is false, the whole conjunction is false
        if not dis_flag:
            return False
    return True

def main(argv):
    if (len(argv) != 3):
        print("Usage: {} <dimacs-problem-file> <solution-file>".format(argv[0]))
        return
    problem_file_name = argv[1]
    solution_file_name = argv[2]
    with open(problem_file_name, 'r') as p_file:
        cnf = solver.parse_dimacs(p_file)
        vals = vals_from_sol(solution_file_name)
        if not vals:
            print('Solution file claims unsatisfiability!')
            return
        if check_solution(cnf, vals):
            print('This is a solution.')
            return
        print('This is NOT a solution.')

if __name__ == '__main__':
    main(sys.argv)
