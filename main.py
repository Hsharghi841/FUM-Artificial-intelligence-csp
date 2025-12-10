#TODO: use nonograpm for testing here

from CSP.Solver import Solver, FastNonogramSolver
from States.StatesProblem import StatesProblem
from Nonogram.NonogramProblem import NonogramProblem

if __name__ == '__main__':
    states = NonogramProblem()
    s = FastNonogramSolver(states)
    s.solve()
    states.print_assignments()