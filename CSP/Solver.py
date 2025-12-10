import os
import subprocess
import time
from collections import deque
from copy import deepcopy
from typing import Optional, List, Set, Tuple

from CSP.Problem import Problem
from CSP.Variable import Variable


class Solver:

    def __init__(self, problem: Problem):
        """
        Initializes the Solver object with the given problem instance and optional parameters.

        Args:
            problem (Problem): The problem instance to be solved.
        """
        self.problem = problem
        self.back_up = deque()

    def is_finished(self) -> bool:
        """
        Determines if the problem has been solved.

        Returns:
            bool: True if the problem has been solved, False otherwise.
        """
        return all([x.is_satisfied() for x in self.problem.constraints]) and len(
            self.problem.get_unassigned_variables()) == 0

    def solve(self):
        """
        Solves the problem instance using the backtracking algorithm with optional heuristics.
        """
        start = time.time()
        result = self.backtracking()
        end = time.time()
        time_elapsed = (end - start) * 1000
        if result:
            print(f'Solved after {time_elapsed} ms')
        else:
            print(f'Failed to solve after {time_elapsed} ms')

    def backtracking(self) -> bool:
        """
        Implements the backtracking algorithm.

        Returns:
            bool: True if the problem has been solved, False otherwise.
        """
        if self.is_finished():
            return True
        var = self.problem.get_unassigned_variables()[0]
        ordered_values = var.domain
        for value in ordered_values:
            self.save_domain(self.problem.variables)
            var.value = value
            if self.is_consistent(var) and self.forward_check(var): 
                result = self.backtracking()
                if result:
                    return True
            var.value = None
            self.load_domain(self.problem) 
        return False

    def forward_check(self, var: Variable) -> bool:
        """
        Implements the Forward Checking algorithm.

        """
        constraints = self.problem.get_constraints(var)

        for neighbor in var.neighbors:
            if neighbor.has_value:
                continue
            tmp = neighbor.domain.copy()
            for value in tmp:
                neighbor.value = value
                for constraint in constraints:
                    if neighbor in constraint.variables:
                        if not constraint.is_satisfied():
                            tmp.remove(value)
                            break                
            neighbor.value = None
            if len(tmp) == 0:
                return False
            else:
                neighbor.domain=tmp              
        return True    

    def is_consistent(self, var: Variable) -> bool:
        """
        Determines ifthe given variable is consistent with all constraints.

        Args:
            var (Variable): The variable to be checked for consistency.

        Returns:
            bool: True if the variable is consistent with all constraints, False otherwise.
        """
        return all(constraint.is_satisfied() for constraint in self.problem.constraints if var in constraint.variables)
    
    def save_domain(self, vars: list[Variable]):
        self.back_up.append([var.domain.copy() for var in vars])
    
    def load_domain(self, problem: Problem):
        domains = self.back_up.pop()
        for i in range(len(problem.variables)):
            problem.variables[i].domain = domains[i]


class FastNonogramSolver:
    """
    fast Nonogram solver using line-solving techniques.
    This uses constraint propagation without backtracking when possible.
    Optimized specifically for Nonogram puzzles.
    """
    
    def __init__(self, problem):
        self.problem = problem
        self.rows = problem.rows if hasattr(problem, 'rows') else problem.size
        self.cols = problem.cols if hasattr(problem, 'cols') else problem.size
        self.grid = problem.grid
        self.constraints = problem.constraints
        self.iterations = 0
        
    def solve(self):
        """
        Solve the nonogram using iterative constraint propagation.
        """
        start = time.time()
        
        print(f"Starting to solve {self.rows}x{self.cols} nonogram...")
        
        # Iterative constraint propagation
        changed = True
        self.iterations = 0
        
        while changed:
            changed = False
            self.iterations += 1
            
            # Process each constraint (row and column)
            for constraint in self.constraints:
                if self._solve_line(constraint):
                    changed = True
            
            # Print progress
            filled = sum(1 for v in self.problem.variables if v.has_value)
            total = len(self.problem.variables)
            print(f"Iteration {self.iterations}: {filled}/{total} cells assigned ({100*filled//total}%)")
            
            if filled == total:
                break
                
            # Prevent infinite loops
            if self.iterations > 100:
                print("Max iterations reached, may need backtracking")
                break
        
        end = time.time()
        time_elapsed = (end - start) * 1000
        
        # Check if solved
        filled = sum(1 for v in self.problem.variables if v.has_value)
        total = len(self.problem.variables)
        
        # Check all constraints
        satisfied = []
        unsatisfied = []
        for i, c in enumerate(self.constraints):
            if c.is_satisfied():
                satisfied.append(i)
            else:
                unsatisfied.append(i)
        
        if filled == total and len(unsatisfied) == 0:
            print(f'✓ Solved after {time_elapsed:.2f} ms ({self.iterations} iterations)')
            return True
        else:
            if filled == total:
                print(f'✗ All cells assigned but {len(unsatisfied)} constraints unsatisfied after {time_elapsed:.2f} ms')
                print(f'  Unsatisfied constraints: {unsatisfied[:10]}...' if len(unsatisfied) > 10 else f'  Unsatisfied constraints: {unsatisfied}')
            else:
                print(f'✗ Partial solution after {time_elapsed:.2f} ms - {filled}/{total} cells ({100*filled//total}%)')
            
            print(f'  Trying backtracking for remaining cells...')
            
            # Use backtracking for remaining cells
            result = self._backtrack()
            end2 = time.time()
            total_time = (end2 - start) * 1000
            
            if result:
                print(f'✓ Fully solved after {total_time:.2f} ms total')
                return True
            else:
                print(f'✗ Could not complete solution')
                return False
    
    def _solve_line(self, constraint) -> bool:
        """
        Solve a single line using fast line-solving algorithm.
        Returns True if any cells were assigned.
        """
        # Import here to avoid circular dependency
        from Nonogram.NonogramConstraint import NonogramConstraint
        
        if not isinstance(constraint, NonogramConstraint):
            return False
            
        variables = constraint.variables
        clue = constraint.clue
        n = len(variables)
        
        # Get current state
        current = [v.value for v in variables]
        
        # If fully assigned, nothing to do
        if None not in current:
            return False
        
        # Generate all valid completions efficiently
        definite_filled, definite_empty = self._find_definite_cells(current, clue, n)
        
        changed = False
        
        # Assign definite cells
        for idx in definite_filled:
            #TODO: Implement Here!
            if variables[idx].value is None:
                variables[idx].value = 1
                changed = True
        
        for idx in definite_empty:
            #TODO: Implement Here!
            if variables[idx].value is None:
                variables[idx].value = 0
                changed = True
        
        return changed
    
    def _find_definite_cells(self, current: List[int], clue: List[int], n: int) -> Tuple[Set[int], Set[int]]:
        """
        Fast algorithm to find cells that must be filled or empty.
        Uses generating all valid solutions and finding common cells.
        """
        if not clue:
            # No filled cells - all must be empty
            empty = set(i for i in range(n) if current[i] is None)
            return set(), empty
        
        # Generate all valid lines that match current state
        valid_lines = self._generate_all_valid_lines(current, clue, n)
        
        if not valid_lines:
            # No valid solution - contradiction
            return set(), set()
        
        definite_filled = set()
        definite_empty = set()
        
        # Find cells that are the same in ALL valid lines
        for i in range(n):
            #TODO: Implement Here!
            if all((s[i] for s in valid_lines)): definite_filled.union(i) 
            if not any((s[i] for s in valid_lines)):definite_empty.union(i) 
        
        return definite_filled, definite_empty
    
    def _generate_all_valid_lines(self, current: List[int], clue: List[int], n: int, max_solutions=1000) -> List[List[int]]:
        """
        Generate all valid line configurations that match the clue and current state.
        Limit to max_solutions for performance.
        """
        valid_lines = []
        
        def place_blocks(pos, clue_idx, line):
            """Recursively place blocks"""
            #TODO: Implement Here! (complete the logic for placing blocks recursively)
        
        place_blocks(0, 0, [None] * n) 
        return valid_lines
    
    def _mrv_select(self, unassigned: List[Variable]) -> Variable:
        """
        Implements Minimum Remaining Values heuristic for FastNonogramSolver.
        Selects the variable with the smallest domain (most constrained).
        
        Args:
            unassigned: List of unassigned variables
            
        Returns:
            Variable with smallest domain
        """
        if not unassigned:
            return None
        
        # For nonogram, domain is [0, 1], so we need a different metric
        # We'll count how many constraints affect each variable
        # and prefer variables that appear in more unsatisfied constraints
        def constraint_score(var):
            """Calculate constraint score - higher means more constrained"""
            #TODO: Implement Here!
            pass
        
        # Sort by most constrained (highest score)
        return max(unassigned, key=constraint_score)
    
    def _lcv_order(self, var: Variable) -> List[int]:
        """
        Implements Least Constraining Value heuristic for FastNonogramSolver.
        Orders domain values [0, 1] by how many conflicts they cause.
        
        Args:
            var: Variable to order values for
            
        Returns:
            List of values ordered by least constraining first
        """
        #TODO: Implement Here!
        pass
    
    def _forward_check(self, var: Variable) -> bool:
        """
        Implements Forward Checking for FastNonogramSolver.
        After assigning a value to var, checks if any constraint involving var
        would eliminate all possible values for unassigned variables.
        
        Args:
            var: The variable that was just assigned
            
        Returns:
            bool: True if forward checking passes (no domain wipeout), False otherwise
        """
        # Get constraints that involve the assigned variable
        related_constraints = [c for c in self.constraints if var in c.variables]
        
        # For each constraint, check if unassigned variables in it still have valid values
        for constraint in related_constraints:
            unassigned_in_constraint = [v for v in constraint.variables if not v.has_value]
            
            for unassigned_var in unassigned_in_constraint:
                # Check if this unassigned variable has any valid value
                has_valid_value = False
                
                for test_value in [0, 1]:
                    unassigned_var.value = test_value
                    
                    # Check if constraint can still be satisfied
                    if constraint.is_satisfied():
                        has_valid_value = True
                        unassigned_var.value = None
                        break
                    
                    unassigned_var.value = None
                
                # If no valid value exists for this variable, forward check fails
                if not has_valid_value:
                    return False
        
        return True
    
    def _backtrack(self) -> bool:
        """
        Backtracking with MRV and LCV heuristics for remaining unassigned cells.
        Uses Minimum Remaining Values to select variables and Least Constraining Value to order domain values.
        """
        #TODO: use your mrv and lcv here!
        
        # Find unassigned variables
        unassigned = [v for v in self.problem.variables if not v.has_value]
        
        # If all assigned, check if satisfied
        if not unassigned:
            return all(c.is_satisfied() for c in self.constraints)
        
        # Select the first unassigned variable
        var = unassigned[0]
        
        # Default order
        ordered_values = [0, 1]
        
        # Try values in order
        for value in ordered_values:
            var.value = value
            
            # Check constraints involving this variable
            related_constraints = [c for c in self.constraints if var in c.variables]
            
            # Check if assignment satisfies constraints and passes forward checking
            if all(c.is_satisfied() for c in related_constraints) and self._forward_check(var):
                # Try propagation
                changed = True
                iterations = 0
                while changed and iterations < 3:
                    changed = False
                    iterations += 1
                    for c in self.constraints:
                        if self._solve_line(c):
                            changed = True
                
                # Recurse
                if self._backtrack():
                    return True
            
            # Backtrack - unassign
            var.value = None
        
        return False
