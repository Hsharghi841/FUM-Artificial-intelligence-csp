#TODO: use nonograpm for testing here

from CSP.Solver import Solver, FastNonogramSolver
from States.StatesProblem import StatesProblem

if __name__ == '__main__':
    states = StatesProblem()
    s = Solver(states)
    s.solve()
    states.print_assignments()