# SAT Solver
This repository contains all the files associated with the Logic in Computer Science project - the SAT solver.

## How to run the presentation test
First and foremost, to run the presentation test, open the terminal, navigate to the ```code/``` directory, and write
```
python3 solver.py test/4000_159410_-7349411764705733428.txt -o test/solution.txt
```
for our solver to solve the 25-colourability problem on a randomly generated graph with 160 vertices and output the solution to ```code/test/solution.txt```. The test should run for between 30 and 40 seconds, depending on your machine. As the file name suggests, the test case has 4000 literals and 159410 clauses.
For the Windows operating system, modify the syntax accordingly.

## How to - general
Our SAT solver implements the DPLL algorithm with both the unit propagation and pure literal elimination optimisations. However, both of the optimisations are entirely optional and can be set not to occur (by default both are turned on). The general syntax for the solver is therefore
```
python3 solver.py <dimacs-file> [-nU] [-nP] [-o <solution-file>]
```
where the ```-nU``` and ```-nP``` flags disable unit propagation and pure literal elimination respectively. This is quite useful in certain cases where pure literal elimination becomes costly and slows the algorithm down, so it is smart to disable it.
If a certain test takes too long, try running it again with the ```-nP``` flag.

While the ```solver.py``` script, if run as a program, automatically verifies the validity of the produced solution, there is also the ```tester.py``` script, that does virtually the same thing. The syntax is
```
python3 tester.py <dimacs-file> <solution-file>
```

The remaining two scripts are for randomly generating test cases and need not be used. The ```randgen.py``` script generates random satisfiable cnf formulas and writes them do Dimacs format text files if they satisfy predetermined time constraints. The general syntax is
```
python3 randgen.py <num-literals> <num-clauses> <max-clause-size> <num-reps>
```
The ```generator.py``` script contains functions for generating cnf formulas for solving the *k*-colourability problem on a given graph. When run as a program, it randomly generates graphs and tests them. The syntax is
```
python3 generator.py <num-vertices> <num-colours> <num-reps>
```

Along with the code, there is also a ```test/``` directory, which contains some of the tests we also found useful during programming, including more colourability problems and a couple of [SATLIB - Benchmark problems](https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html) and [ToughSAT](https://toughsat.appspot.com/) problems, but they also need not be run. (**Warning**: SATLIB problems are usually double-spaced, so modify the parse_dimacs function in solver.py.)

# Authors
- Benjamin Benčina,
- Kerem Güneş,
- Petra Podlogar.
