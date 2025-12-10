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

    def _is_partially_consistent(self, values: List[int]) -> bool:
        """
        Check if a partial assignment could potentially satisfy the constraint.
        This allows for early pruning during search.
        Optimized version that checks basic consistency without generating all placements.
        """
        # TODO: Implement Here! (complete the logic for partial consistency check)

        # If no clue, no filled cells allowed
        if not self.clue:
            return all(v != 1 for v in values)

        # Quick checks for obvious violations

        # 1. Check if we have too many filled cells
        filled_count = sum(1 for v in values if v == 1)
        total_filled_needed = sum(self.clue)
        if filled_count > total_filled_needed:
            return False

        # 2. Check if we have too many empty cells in wrong places
        # (This is a simplified check - full implementation would be more complex)

        # 3. Check pattern consistency
        return self._check_pattern_consistency(values)

    def _check_pattern_consistency(self, values: List[int]) -> bool:
        """
        Check if the current pattern could possibly match the clue.
        """
        # Group the values into blocks
        groups = []
        current_group = 0
        in_group = False

        for v in values:
            if v == 1:
                if not in_group:
                    in_group = True
                    current_group = 1
                else:
                    current_group += 1
            elif v == 0:
                if in_group:
                    groups.append(current_group)
                    in_group = False
                    current_group = 0
            else:  # v is None (unknown)
                # Unknown cell - we can't determine group boundaries definitively
                # So we need to be more flexible
                if in_group:
                    # Could continue the group or end it
                    current_group += 1  # Assume it continues for now
                # else: could start a group or remain empty

        # Handle last group if we ended in one
        if in_group:
            groups.append(current_group)

        # Check if the groups we found are compatible with the clue
        # We can't reject based on number of groups because unknown cells
        # might create new groups or merge existing ones

        # Check each group against corresponding clue
        for i in range(min(len(groups), len(self.clue))):
            if groups[i] > self.clue[i]:
                return False

        return True

    def _matches_clue(self, values: List[int]) -> bool:
        """
        Check if a complete assignment matches the clue exactly.
        """
        # TODO: Implement Here! (complete the logic for matching the clue)

        # Convert to string for easier processing
        line_str = ''.join(['1' if v == 1 else '0' for v in values])

        # If no clue, line should be all 0s
        if not self.clue:
            return all(v == 0 for v in values)

        # Split by one or more zeros to get groups of ones
        groups = []
        current_group = 0

        for v in values:
            if v == 1:
                current_group += 1
            elif v == 0:
                if current_group > 0:
                    groups.append(current_group)
                    current_group = 0

        # Don't forget the last group
        if current_group > 0:
            groups.append(current_group)

        # Check if groups match the clue exactly
        return groups == self.clue