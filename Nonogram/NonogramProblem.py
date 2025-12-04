from typing import List
from CSP.Problem import Problem
from CSP.Variable import Variable
from Nonogram.NonogramConstraint import NonogramConstraint


class NonogramProblem(Problem):
    """
    A Nonogram puzzle as a CSP.
    Each cell can be either 0 (empty) or 1 (filled).
    Row and column clues specify the pattern of filled cells.
    """
    
    def __init__(self):
        """
        Initialize a Nonogram problem.
        """
        super().__init__([], [], "Dolphin Nonogram (25x25)")
        self._init_dolphin_25x25()
    
    def _init_dolphin_25x25(self):
        """Initialize the full 25x25 dolphin puzzle."""
        self.rows = 25
        self.cols = 25
        self.size = 25  # For backward compatibility
        
        # Define row clues (from top to bottom) - Full dolphin pattern
        row_clues = [
            [8],
            [7, 3],
            [16],
            [11, 4],
            [13, 2],
            [14, 2],
            [18],
            [8, 4],
            [6, 4],
            [5, 5],
            [4, 2, 2],
            [4, 3, 1],
            [3, 2, 1],
            [3, 2],
            [3, 2],
            [2, 1, 4],
            [2, 1, 4],
            [2, 1, 4],
            [3, 1, 4],
            [5, 4],
            [11],
            [10],
            [5],
            [5],
            [6],
        ]
        
        # Define column clues (from left to right)
        column_clues = [
            [1],
            [2],
            [2],
            [4],
            [11],
            [13],
            [15],
            [9, 3],
            [8, 3],
            [7, 5, 2],
            [7, 3, 4],
            [6, 2, 3],
            [8, 3, 2],
            [13, 2],
            [10, 2],
            [5, 5, 3],
            [4, 1, 4, 6],
            [1, 2, 2, 8],
            [3, 1, 10],
            [3, 1, 4, 4],
            [2, 1, 2, 3],
            [2, 1, 2],
            [2, 1],
            [2, 1],
            [1],
        ]
        
        self._create_grid_and_constraints(row_clues, column_clues)
    
    def _create_grid_and_constraints(self, row_clues, column_clues):
        """Create the grid variables and constraints."""
        #TODO: Implement Here!
        pass
    
    def print_board(self):
        """
        Print the current state of the nonogram board.
        Uses █ for filled cells (1), ░ for empty cells (0), and · for unassigned cells.
        """
        print(f"\n{self.name} - Current Board ({self.rows}x{self.cols}):")
        
        # Print column numbers header
        if self.cols <= 20:
            # Small board - use spaced format
            print("  ", end="")
            for col in range(self.cols):
                print(f" {col}", end="")
            print()
            
            for row in range(self.rows):
                print(f"{row:2d}", end="")
                for col in range(self.cols):
                    value = self.grid[row][col].value
                    if value == 1:
                        print(" █", end="")
                    elif value == 0:
                        print(" ░", end="")
                    else:
                        print(" ·", end="")
                print()
        else:
            # Large board - use compact format
            print("    ", end="")
            for col in range(self.cols):
                print(f"{col%10}", end="")
            print()
            
            for row in range(self.rows):
                print(f"{row:2d} ", end="")
                for col in range(self.cols):
                    value = self.grid[row][col].value
                    if value == 1:
                        print("█", end="")
                    elif value == 0:
                        print("░", end="")
                    else:
                        print("·", end="")
                print()
        print()
    
    def print_assignments(self):
        """
        Override to provide a nicer output for the nonogram.
        """
        self.print_board()
