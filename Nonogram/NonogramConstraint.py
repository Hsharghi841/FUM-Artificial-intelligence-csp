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
        self.line_length = len(variables)
        if clue:
            self.min_length = sum(clue) + len(clue) - 1
        else:
            self.min_length = 0
    
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
        
        if not self.clue:
            
            return all(v != 1 for v in values)
        
    
        line = ''.join(['1' if v == 1 else '0' if v == 0 else '?' for v in values])
        possible_placements = self._generate_possible_placements(len(values), self.clue)
    
        for placement in possible_placements:
            if self._placement_matches(line, placement):
                return True
        return False
    def _generate_possible_placements(self, length: int, clue: List[int]) -> List[str]:
        placements = []
        self._generate_placements_recursive(length, clue, 0, 0, [], placements)
        return placements
    
    def _generate_placements_recursive(self, length: int, clue: List[int], clue_idx: int, 
                                      position: int, current: List[str], placements: List[str]):
        if clue_idx == len(clue):
            placements.append(''.join(current) + '0' * (length - position))
            return
        
        clue_size = clue[clue_idx]
        
        for start in range(position, length - clue_size + 1):
            if '0' in ''.join(current)[start:start + clue_size]:
                continue
                
            new_current = current + ['0' * (start - position)] + ['1' * clue_size]
            
            if clue_idx < len(clue) - 1:
                new_current.append('0')
                next_position = start + clue_size + 1
            else:
                next_position = start + clue_size
            
            self._generate_placements_recursive(length, clue, clue_idx + 1, next_position, new_current, placements)
    
    def _placement_matches(self, line: str, placement: str) -> bool:
        if len(line) != len(placement):
            return False
            
        for i in range(len(line)):
            if line[i] == '?':
                continue
            if line[i] != placement[i]:
                return False
        return True
    def _matches_clue(self, values: List[int]) -> bool:
        
        line_str = ''.join(['1' if v == 1 else '0' for v in values])
        
        if not self.clue:
            return all(v == 0 for v in values)
        
        groups = [group for group in line_str.split('0') if group]
        
        if len(groups) != len(self.clue):
            return False
        
        for i in range(len(groups)):
            if len(groups[i]) != self.clue[i]:
                return False
        
        return True