from typing import List, Set, Tuple
from CSP.Constraint import Constraint
from CSP.Variable import Variable


class NonogramConstraint(Constraint):
    """
    Constraint for a Nonogram puzzle row or column.
    Checks if the sequence of filled cells matches the given clue.
    Optimized with line-solving techniques.
    """
    
    def __init__(self, variables: List[Variable], clue: List[int]):
        """
        Args:
            variables: List of variables representing a row or column
            clue: List of integers indicating consecutive filled cells
                  e.g., [2, 3] means 2 filled cells, then 3 filled cells with at least 1 gap
        """
        super().__init__(variables)
        self.clue = clue
        self.line_length = #TODO: Implement Here!
        self.min_length = #TODO: Implement Here!
    
    def is_satisfied(self) -> bool:
        """
        Check if the current assignment satisfies the nonogram constraint.
        Returns True if all variables are assigned and match the clue,
        or if not all variables are assigned yet (partial consistency check).
        """
        # Get the values of all variables (None if unassigned, 0 or 1 if assigned)
        values = [var.value for var in self.variables]
        
        # If not all variables are assigned, check partial consistency
        if None in values:
            return self._is_partially_consistent(values)
        
        # All variables assigned - check full consistency
        return self._matches_clue(values)
    
    def _is_partially_consistent(self, values: List[int]) -> bool:
        """
        Check if a partial assignment could potentially satisfy the constraint.
        This allows for early pruning during search.
        Optimized version with better pruning.
        """
        if not self.clue:
            # Empty clue - no filled cells allowed
            return all(v != 1 for v in values)
        
       #TODO: Implement Here! (complete the logic for partial consistency check)
       pass
    
    def _matches_clue(self, values: List[int]) -> bool:
        """
        Check if a complete assignment matches the clue exactly.
        """
       #TODO: Implement Here! (complete the logic for matching the clue)
       pass 
