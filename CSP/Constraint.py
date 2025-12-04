from abc import ABC, abstractmethod
from CSP.Variable import Variable

class Constraint(ABC):

    def __init__(self, variables: list[Variable]):
        self.variables = variables

    @abstractmethod
    def is_satisfied(self) -> bool:
        return True


class SoftConstraint(ABC):
    """
    A soft constraint (preference) that should be satisfied if possible,
    but doesn't have to be satisfied for a valid solution.
    Used to guide the solver towards better solutions.
    """
    
    def __init__(self, variables: list[Variable], weight: float = 1.0):
        self.variables = variables
        self.weight = weight  # Higher weight = more important preference
    
    @abstractmethod
    def is_satisfied(self) -> bool:
        """Check if the preference is satisfied."""
        return True
    
    def get_violation_cost(self) -> float:
        """
        Returns the cost of violating this preference.
        0 if satisfied, weight if violated.
        """
        return 0.0 if self.is_satisfied() else self.weight
    





