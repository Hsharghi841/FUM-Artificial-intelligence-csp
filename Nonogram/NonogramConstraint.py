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
        Optimized version with better pruning.
        """
        # TODO: Implement Here! (complete the logic for partial consistency check)

        if not self.clue:
            return all(v != 1 for v in values)


        filled_count = sum(1 for v in values if v == 1)
        total_filled_needed = sum(self.clue)
        if filled_count > total_filled_needed:
            return False

        empty_count = sum(1 for v in values if v == 0)
        total_empty_needed = self.line_length - total_filled_needed
        if empty_count > total_empty_needed:
            return False

        return self._dp_check_possible(values)

    def _dp_check_possible(self, values: List[int]) -> bool:
        """
        Use dynamic programming to check if any valid placement exists.
        Returns True if at least one valid placement is possible.
        """
        n = len(values)
        m = len(self.clue)

        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True

        for i in range(n + 1):
            for j in range(m + 1):
                if not dp[i][j]:
                    continue

                if i < n and values[i] != 1:
                    dp[i + 1][j] = True

                if j < m and i < n and values[i] != 0:
                    block_len = self.clue[j]

                    can_place = True
                    for k in range(block_len):
                        if i + k >= n:
                            can_place = False
                            break
                        if values[i + k] == 0:
                            can_place = False
                            break

                    if can_place:
                        next_pos = i + block_len
                        if j == m - 1:
                            dp[next_pos][j + 1] = True
                        elif next_pos < n and values[next_pos] != 1:
                            dp[next_pos + 1][j + 1] = True

        return dp[n][m]

    def _matches_clue(self, values: List[int]) -> bool:
        """
        Check if a complete assignment matches the clue exactly.
        """


        processed_values = []
        for v in values:
            if v is None:
                return False
            processed_values.append(v)

        if not self.clue:
            return all(v == 0 for v in processed_values)

        blocks = []
        current_block = 0

        for v in processed_values:
            if v == 1:
                current_block += 1
            elif current_block > 0:
                blocks.append(current_block)
                current_block = 0

        if current_block > 0:
            blocks.append(current_block)

        return blocks == self.clue